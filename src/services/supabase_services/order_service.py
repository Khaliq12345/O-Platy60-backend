# order_service.py

import datetime
from src.services.supabase_services.supabase_service import SupabaseService
from typing import Any


class OrdersService(SupabaseService):
    def __init__(self) -> None:
        super().__init__()

    def get_orders(
        self,
        status: str | None = None,
        ingredient_id: str | None = None,
        created_at: str | None = None,
        completed_at: str | None = None,
        page: int = 1,
        limit: int = 10,
    ) -> dict[str, Any] | None:
        """Récupère la liste des commandes avec filtres et pagination"""
        query = self.client.table("orders").select("*, ingredients(*)", count="exact")
        # Application des filtres
        query = query.eq("delete", False)
        if status:
            query = query.eq("status", status)
        if ingredient_id:
            query = query.eq("ingredient_id", ingredient_id)
        # Filtres sur dates de création
        if created_at:
            query = query.gte("created_at", created_at)
        if completed_at:
            query = query.gte("completed_at", completed_at)

        # Calcul de l'offset pour la pagination
        offset = (page - 1) * limit
        # Exécution de la requête unique avec pagination
        response = query.range(offset, offset + limit - 1).execute()

        # Vérification de la réponse
        if not response:
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

    def create_order(self, order_data: dict[str, Any]) -> dict[str, Any] | None:
        """Crée une nouvelle commande d'ingrédient"""
        # Insertion de la commande
        order_dict = {k: v for k, v in order_data.items() if v is not None}
        print(order_dict)
        order_response = self.client.table("orders").insert(order_dict).execute()
        # Récupération de la commande créée
        result = order_response.data
        if result:
            return result[0]

    def get_order_by_id(self, order_id: int) -> dict[str, Any] | None:
        """Récupère une commande par son ID avec l'ingrédient"""
        response = (
            self.client.table("orders")
            .select("*, ingredients(*)")
            .eq("id", order_id)
            .eq("delete", False)
            .single()
            .execute()
        )
        if response.data:
            return response.data

    def update_order(
        self, order_id: int, update_data: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Met à jour une commande existante"""
        update_dict = {k: v for k, v in update_data.items() if v is not None}
        update_dict["last_updated"] = datetime.now().isoformat()

        if update_dict:
            response = (
                self.client.table("orders")
                .update(update_dict)
                .eq("id", order_id)
                .execute()
            )
            if response.data:
                return response.data[0]

    def soft_delete_order(self, order_id: int) -> dict[str, str] | None:
        """Effectue une suppression logique de la commande"""
        # Suppression logique
        result = (
            self.client.table("orders")
            .update({"delete": True, "last_updated": datetime.now().isoformat()})
            .eq("id", order_id)
            .execute()
        )
        if result.data:
            return result.data[0]

    def get_ingredient_orders(self, sku: str, sort: str, limit: int):
        """Récupère les commandes d'un ingredient"""
        desc = True if sort == "descending" else False
        response = (
            self.client.table("orders")
            .select("*")
            .eq("ingredient_id", sku)
            .eq("delete", False)
            .limit(limit)
            .order("created_at", desc=desc)
            .execute()
        )
        if response.data:
            return response.data
