"""Database layer for Marco user profiles and recipe history."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from marco.config import settings
from marco.schemas import Recipe, UserProfile


class Database:
    """SQLite database manager."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database connection."""
        self.db_path = db_path or settings.database_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

    def close(self):
        """Close database connection."""
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def save_recipe(self, recipe: Recipe) -> int:
        """Save a recipe to the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO recipes (
                name, description, prep_time, cook_time, servings,
                ingredients, instructions, nutrition, psychonutrition_analysis,
                tags, difficulty, cuisine, season, chef_tips,
                storage_instructions, variations, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                recipe.name,
                recipe.description,
                recipe.prep_time,
                recipe.cook_time,
                recipe.servings,
                json.dumps([i.model_dump() for i in recipe.ingredients]),
                json.dumps(recipe.instructions),
                json.dumps(recipe.nutrition.model_dump())
                if recipe.nutrition
                else None,
                json.dumps(recipe.psychonutrition_analysis.model_dump())
                if recipe.psychonutrition_analysis
                else None,
                json.dumps(recipe.tags),
                recipe.difficulty,
                recipe.cuisine,
                recipe.season,
                json.dumps(recipe.chef_tips),
                recipe.storage_instructions,
                json.dumps(recipe.variations),
                datetime.now().isoformat(),
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_recipe(self, recipe_id: int) -> Optional[Recipe]:
        """Get a recipe by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._row_to_recipe(row)

    def list_recipes(self, limit: int = 50, offset: int = 0) -> List[Recipe]:
        """List recent recipes."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM recipes 
            ORDER BY created_at DESC 
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        return [self._row_to_recipe(row) for row in cursor.fetchall()]

    def _row_to_recipe(self, row: sqlite3.Row) -> Recipe:
        """Convert database row to Recipe object."""
        from marco.schemas import Ingredient, NutrientInfo, PsychonutritionAnalysis

        return Recipe(
            name=row["name"],
            description=row["description"],
            prep_time=row["prep_time"],
            cook_time=row["cook_time"],
            servings=row["servings"],
            ingredients=[Ingredient(**i)
                         for i in json.loads(row["ingredients"])],
            instructions=json.loads(row["instructions"]),
            nutrition=NutrientInfo(**json.loads(row["nutrition"])),
            psychonutrition_analysis=PsychonutritionAnalysis(
                **json.loads(row["psychonutrition_analysis"]))
            if row["psychonutrition_analysis"]
            else None,
            tags=json.loads(row["tags"]),
            difficulty=row["difficulty"],
            cuisine=row["cuisine"],
            season=row["season"],
            chef_tips=json.loads(row["chef_tips"]),
            storage_instructions=row["storage_instructions"],
            variations=json.loads(row["variations"]),
        )

    def save_user_profile(self, profile: UserProfile) -> None:
        """Save or update user profile."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO user_profiles (
                user_id, dietary_restrictions, anxiety_symptoms,
                favorite_cuisines, disliked_ingredients, region,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                profile.user_id,
                json.dumps(profile.dietary_restrictions),
                json.dumps(profile.anxiety_symptoms),
                json.dumps(profile.favorite_cuisines),
                json.dumps(profile.disliked_ingredients),
                profile.region,
                profile.created_at.isoformat(),
                datetime.now().isoformat(),
            ),
        )
        self.conn.commit()

    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None

        return UserProfile(
            user_id=row["user_id"],
            dietary_restrictions=json.loads(row["dietary_restrictions"]),
            anxiety_symptoms=json.loads(row["anxiety_symptoms"]),
            favorite_cuisines=json.loads(row["favorite_cuisines"]),
            disliked_ingredients=json.loads(row["disliked_ingredients"]),
            region=row["region"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )


def init_db(db_path: Optional[Path] = None) -> None:
    """Initialize database schema."""
    db_path = db_path or settings.database_path
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Create recipes table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            prep_time INTEGER,
            cook_time INTEGER,
            servings INTEGER,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            nutrition TEXT,
            psychonutrition_analysis TEXT,
            tags TEXT,
            difficulty TEXT,
            cuisine TEXT,
            season TEXT,
            chef_tips TEXT,
            storage_instructions TEXT,
            variations TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    # Create user profiles table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            dietary_restrictions TEXT,
            anxiety_symptoms TEXT,
            favorite_cuisines TEXT,
            disliked_ingredients TEXT,
            region TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    # Create indexes
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_recipes_created ON recipes(created_at)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_recipes_cuisine ON recipes(cuisine)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_recipes_season ON recipes(season)")

    conn.commit()
    conn.close()
