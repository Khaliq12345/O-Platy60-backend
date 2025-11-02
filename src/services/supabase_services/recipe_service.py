from datetime import datetime
from src.services.supabase_services.supabase_service import SupabaseService
from typing import Any


class RecipeService(SupabaseService):
    def __init__(self) -> None:
        super().__init__()
        self.recipe_table = "recipes"

    def get_recipes(
        self,
        active: bool | str,
        category: str | None,
        search_query: str | None,
        page: int = 1,
        limit: int = 10,
    ) -> dict[str, Any] | None:
        """Récupère la liste des plats avec filtres et pagination"""
        query = self.client.table(self.recipe_table).select("*", count="exact")
        # Application des filtres
        query = query.eq("delete", False)
        if active != "all":
            query = query.eq("active", active)
        if search_query:
            query = query.ilike("name", f"%{search_query}%")
        if (category) and (category != "all"):
            query = query.eq("category", category)

        # Calcul de l'offset pour la pagination
        offset = (page - 1) * limit
        # Exécution de la requête unique avec pagination
        response = query.range(offset, offset + limit - 1).execute()

        # Vérification de la réponse
        if not response.data:
            return None

        # On s'assure que total est un entier
        total = response.count if response.count is not None else 0
        return {
            "data": response.data,
            "requests": {
                "total": total,
                "page": page,
                "limit": limit,
                "has_next": offset + limit < total,
                "has_prev": page > 1,
            },
        }

    def create_recipe(self, recipe_data: dict) -> dict[str, Any] | None:
        """Crée une nouvelle Repat"""
        # Insertion de la commande
        update_dict = {k: v for k, v in recipe_data.items() if v is not None}
        recipe_response = (
            self.client.table(self.recipe_table).insert(update_dict).execute()
        )
        # Récupération de la commande créée
        result = recipe_response.data
        if result:
            return result[0]

    def get_recipe_by_id(self, recipe_id: int) -> dict[str, Any] | None:
        """Récupère un repat par son ID"""
        response = (
            self.client.table(self.recipe_table)
            .select("*")
            .eq("id", recipe_id)
            .eq("delete", False)
            .single()
            .execute()
        )
        if response.data:
            return response.data

    def update_recipe(
        self, recipe_id: int, update_data: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Met à jour un repat existante"""
        update_dict = {k: v for k, v in update_data.items() if v is not None}
        update_dict["last_updated"] = datetime.now().isoformat()
        if update_dict:
            response = (
                self.client.table(self.recipe_table)
                .update(update_dict)
                .eq("id", recipe_id)
                .execute()
            )
            if response.data:
                return response.data[0]

    def soft_delete_recipe(self, recipe_id: int) -> dict[str, str] | None:
        """Effectue une suppression logique de la repat"""
        # Suppression logique
        result = (
            self.client.table(self.recipe_table)
            .update({"delete": True, "last_updated": datetime.now().isoformat()})
            .eq("id", recipe_id)
            .execute()
        )
        if result.data:
            return result.data[0]

    def get_ingredients_of_recipe(self, recipe_id: int) -> dict[str, str]:
        """Récupère les ingredients d'un repat"""
        result = (
            self.client.table("recipes_ingredients")
            .select("*, ingredients(name,sku,unit,unit_cost)")
            .eq("recipe_id", recipe_id)
            .execute()
        )
        # Parse the output and match the ingredient correctly
        response = result.data
        ingredients = []
        for x in response:
            ingredient = x["ingredients"]
            ingredients.append(
                {
                    "name": ingredient["name"],
                    "sku": ingredient["sku"],
                    "unit": ingredient["unit"],
                    "unit_cost": ingredient["unit_cost"],
                    "quantity": x["quantity_being_used"],
                }
            )
        return {"recipe_id": recipe_id, "ingredients": ingredients}

    def add_ingredient_to_recipe(
        self, recipe_id: int, ingredient_sku: str, quantity: float
    ):
        """Add Ingredient to a recipe"""
        response = (
            self.client.table("recipes_ingredients")
            .insert(
                {
                    "recipe_id": recipe_id,
                    "ingredient_sku": ingredient_sku,
                    "quantity_being_used": quantity,
                }
            )
            .execute()
        )
        if response.data:
            return response.data[0]

    def edit_ingredient_quantity(
        self, recipe_id: int, ingredient_sku: str, quantity: float
    ):
        """Edit the quantity of ingredient in recipe"""
        response = (
            self.client.table("recipes_ingredients")
            .update({"quantity_being_used": quantity})
            .eq("recipe_id", recipe_id)
            .eq("ingredient_sku", ingredient_sku)
            .execute()
        )
        if response.data:
            return response.data[0]
