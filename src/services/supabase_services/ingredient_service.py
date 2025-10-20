from src.services.supabase_services.supabase_service import SupabaseService
from datetime import datetime
from typing import Dict


class IngredientService(SupabaseService):
    def __init__(self) -> None:
        super().__init__()

    def _serialize_dates(self, data: Dict) -> Dict:
        """Convert datetime objects to ISO strings for Supabase"""
        for key in ["last_received", "last_updated", "expire_at"]:
            if key in data and isinstance(data[key], datetime):
                data[key] = data[key].isoformat()
        return data

    def get_ingredients(self):
        result = (
            self.client.table("ingredients").select("*").eq("delete", False).execute()
        )
        return result.data

    def get_ingredient(self, sku: str):
        result = (
            self.client.table("ingredients")
            .select("*")
            .eq("sku", sku)
            .single()
            .execute()
        )
        return result.data

    def create_ingredient(self, data: dict):
        data["last_updated"] = datetime.utcnow()
        data = self._serialize_dates(data)
        result = self.client.table("ingredients").insert(data).execute()
        return result.data

    def update_ingredient(self, sku: str, data: dict):
        data["last_updated"] = datetime.utcnow()
        data = self._serialize_dates(data)
        result = self.client.table("ingredients").update(data).eq("sku", sku).execute()
        return result.data

    def delete_ingredient(self, sku: str):
        """Suppression logique → delete=True"""
        data = {"delete": True, "last_updated": datetime.utcnow()}
        data = self._serialize_dates(data)
        result = self.client.table("ingredients").update(data).eq("sku", sku).execute()
        return result.data

    def adjust_stock(self, sku: str, quantity: float):
        """Ajuste rapidement le stock"""
        ingredient = self.get_ingredient(sku)
        if not ingredient:
            return None
        new_stock = ingredient["current_stock_level"] + quantity
        data = {"current_stock_level": new_stock, "last_updated": datetime.utcnow()}
        data = self._serialize_dates(data)
        result = self.client.table("ingredients").update(data).eq("sku", sku).execute()
        return result.data

    # placeholders
    def get_history(self, sku: str):
        return []

    def get_batches(self, sku: str):
        return []
