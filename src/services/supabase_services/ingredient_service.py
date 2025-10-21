from src.services.supabase_services.supabase_service import SupabaseService
from datetime import date, datetime
from typing import Any


class IngredientService(SupabaseService):
    def __init__(self) -> None:
        super().__init__()

    def get_ingredients(
        self,
        page: int = 1,
        limit: int = 10,
    ) -> dict[str, Any] | None:
        """Récupère la liste des ingrédients (delete=False) avec pagination"""
        try:
            # Calcul de l'offset pour la pagination
            offset = (page - 1) * limit

            # Construction de la requête
            query = self.client.table("ingredients").select("*", count="exact")
            query = query.eq("delete", False)

            # Exécution avec pagination
            response = query.range(offset, offset + limit - 1).execute()

            if not response:
                return None

            total = response.count if response.count is not None else 0

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
        update_dict = {}
        for k, v in data.items():
            if v is not None:
                update_dict[k] = v

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
