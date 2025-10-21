# order_service.py

from src.services.supabase_services.supabase_service import SupabaseService
from typing import Any, Optional


class OrdersService(SupabaseService):
    def __init__(self) -> None:
        super().__init__()

    def get_orders(
        self,
        status: str | None = None,
        ingredient_id: str | None = None,
        page: int = 1,
        limit: int = 10,
    ) -> Optional[dict[str, Any]]:
        """Récupère la liste des commandes avec filtres et pagination"""
        query = self.client.table("orders").select("*, ingredients(*)", count="exact")
        # Application des filtres
        query = query.eq("delete", False)
        if status:
            query = query.eq("status", status)
        if ingredient_id:
            query = query.eq("ingredient_id", ingredient_id)

        # Calcul de l'offset pour la pagination
        offset = (page - 1) * limit
        # Exécution de la requête unique avec pagination
        response = query.range(offset, offset + limit - 1).execute()

        # Vérification de la réponse
        if not response:
            return None

        # On s'assure que 'total' est un entier pour éviter une erreur de type plus loin
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

    def create_order(self, order_data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Crée une nouvelle commande d'ingrédient"""
        # Insertion de la commande
        order_response = self.client.table("orders").insert(order_data).execute()
        # Récupération de la commande créée
        result = order_response.data
        if result:
            return result[0]

    def get_order_by_id(self, order_id: int) -> Optional[dict[str, Any]]:
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
    ) -> Optional[dict[str, Any]]:
        """Met à jour une commande existante"""
        update_dict = {}
        for k, v in update_data.items():
            if v is not None:
                update_dict[k] = v

        if update_dict:
            response = (
                self.client.table("orders")
                .update(update_dict)
                .eq("id", order_id)
                .execute()
            )
            if response.data:
                return response.data[0]

    def soft_delete_order(self, order_id: int) -> Optional[dict[str, str]]:
        """Effectue une suppression logique de la commande"""
        # Suppression logique
        result = (
            self.client.table("orders")
            .update({"delete": True})
            .eq("id", order_id)
            .execute()
        )
        if result.data:
            return result.data[0]
