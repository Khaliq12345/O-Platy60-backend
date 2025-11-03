from src.services.supabase_services.supabase_service import SupabaseService
from datetime import datetime
from typing import Any


class IngredientService(SupabaseService):
    def __init__(self) -> None:
        super().__init__()

    def get_ingredients(
        self,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        category: str | None = None,
        status: str | None = None,
        low_stock_only: bool | None = False,
    ) -> dict[str, Any] | None:
        """Récupère la liste des ingrédients avec pagination et filtres dynamiques"""
        offset = (page - 1) * limit
        # Base query
        query = self.client.table("ingredients").select("*", count="exact")
        query = query.eq("delete", False)
        # Filtre par catégorie
        if category:
            query = query.eq("category", category)
        # Filtre par statut
        if status:
            query = query.eq("status", status)
        # Filtre low stock
        if low_stock_only:
            query = query.eq("status", "low")
        # Recherche textuelle (name, sku)
        if search:
            query = query.or_(f"name.ilike.%{search}%,sku.ilike.%{search}%")
        print(
            "[get_ingredients] Final query filters:",
            {
                "search": search,
                "category": category,
                "status": status,
                "offset": offset,
            },
        )
        # Pagination
        response = query.range(offset, offset + limit - 1).execute()
        if not response:
            return None
        total = response.count or 0
        return {
            "data": response.data,
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "has_next": offset + limit < total,
                "has_prev": page > 1,
            },
        }

    def get_ingredient(self, sku: str):
        result = (
            self.client.table("ingredients")
            .select("*")
            .eq("sku", sku)
            .single()
            .execute()
        )
        return result.data

    def create_ingredient(self, data: dict[str, Any]):
        update_dict = {k: v for k, v in data.items() if v is not None}
        result = self.client.table("ingredients").insert(update_dict).execute()
        if result.data:
            return result.data[0]

    def update_ingredient(self, sku: str, data: dict[str, Any]):
        update_dict = {k: v for k, v in data.items() if v is not None}
        update_dict["last_updated"] = datetime.now().isoformat()
        result = (
            self.client.table("ingredients")
            .update(update_dict)
            .eq("sku", sku)
            .execute()
        )
        if result.data:
            return result.data[0]

    def adjust_ingredient(self, sku: str, quantity: int):
        """AJouter au stock"""
        result = self.client.rpc(
            "add_quantity_to_ingredient",
            {"p_product_sku": sku, "p_quantity_to_add": quantity},
        ).execute()
        if result.data:
            return result.data[0]

    def delete_ingredient(self, sku: str):
        """Suppression logique → delete=True"""
        data = {"delete": True, "last_updated": datetime.now().isoformat()}
        result = self.client.table("ingredients").update(data).eq("sku", sku).execute()
        if result.data:
            return result.data[0]

    def adjust_stock(self, adjust_dict: dict[str, Any]):
        """Ajuste rapidement le stock"""
        update_dict = {k: v for k, v in adjust_dict.items() if v is not None}
        result = self.client.table("stock_adjustments").insert(update_dict).execute()
        if result.data:
            return result.data[0]

    def search_ingredient(self, keyword: str):
        """Search for an ingredients"""
        results = self.client.rpc(
            "search_ingredients", params={"search_term": keyword}
        ).execute()
        if results.data:
            return results.data

    # placeholders
    def get_history(self, sku: str):
        return []

    def get_batches(self, sku: str):
        return []

    def get_recipes(self, sku: str):
        """Get the recipes that uses this ingredient"""
        results = (
            self.client.table("recipes_ingredients")
            .select("*, recipes(name, cost, category, id)")
            .eq("ingredient_sku", sku)
            .execute()
        )
        recipes = []
        for ingredient in results.data:
            recipe = ingredient["recipes"]
            recipes.append(
                {
                    "name": recipe["name"],
                    "cost": recipe["cost"],
                    "category": recipe["category"],
                    "id": recipe["id"],
                }
            )
        return {"sku": sku, "recipes": recipes}
