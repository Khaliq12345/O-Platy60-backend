from src.services.supabase_services.supabase_service import SupabaseService
from datetime import datetime
from typing import Any
import json


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
        try:
            offset = (page - 1) * limit

            # Base query
            query = self.client.table("ingredients").select("*", count="exact")
            query = query.eq("delete", False)

            # Filtre par catégorie
            if category:
                if category.startswith("{"):
                    category = json.loads(category).get("value", "")
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
                search = search.lower().strip()
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

        except Exception as e:
            print(f"[get_ingredients] Error: {e}")
            return None

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
        result = self.client.table("ingredients").insert(data).execute()
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

    def delete_ingredient(self, sku: str):
        """Suppression logique → delete=True"""
        data = {"delete": True, "last_updated": datetime.now().isoformat()}
        result = self.client.table("ingredients").update(data).eq("sku", sku).execute()
        if result.data:
            return result.data[0]

    def adjust_stock(self, sku: str, quantity: float):
        """Ajuste rapidement le stock"""
        ingredient = self.get_ingredient(sku)
        if not ingredient:
            return None

        now_date = datetime.now().isoformat()
        new_stock = ingredient["current_stock_level"] + quantity
        data = {
            "current_stock_level": new_stock,
            "last_updated": now_date,
            "last_received": now_date,
        }
        result = self.client.table("ingredients").update(data).eq("sku", sku).execute()
        if result.data:
            return result.data[0]

    # placeholders
    def get_history(self, sku: str):
        return []

    def get_batches(self, sku: str):
        return []
