# order_service.py

from src.services.supabase_services.supabase_service import SupabaseService
from typing import Any
from datetime import datetime, timezone


class OrdersService(SupabaseService):
    def __init__(self) -> None:
        super().__init__()

    def validate_order_business_rules(self, order_data: dict[str, Any]) -> None:
        # Valide les règles métier d'une commande
        quantity_ordered = order_data.get("quantity_ordered")
        unit_price_ordered = order_data.get("unit_price_ordered")
        value_ordered = order_data.get("value_ordered")
        
        # Vérifier que la quantité commandée est positive
        if quantity_ordered is not None and quantity_ordered <= 0:
            raise ValueError("La quantité commandée doit être positive")
        
        # Vérifier que le prix unitaire est positif
        if unit_price_ordered is not None and unit_price_ordered < 0:
            raise ValueError("Le prix unitaire commandé ne peut pas être négatif")
        
        # Vérifier que la valeur commandée est cohérente
        if value_ordered is not None and value_ordered < 0:
            raise ValueError("La valeur commandée ne peut pas être négative")
        
        # Vérifier la cohérence entre quantité, prix unitaire et valeur
        # code modifié pour corriger l"erreur : Operator "*" not supported for "None
        if all([quantity_ordered is not None, unit_price_ordered is not None, value_ordered is not None]):
            # À ce stade, on sait que les valeurs ne sont pas None
            assert quantity_ordered is not None
            assert unit_price_ordered is not None
            assert value_ordered is not None
            
            expected_value = quantity_ordered * unit_price_ordered
            if abs(value_ordered - expected_value) > 0.01:  # Tolérance pour les arrondis
                raise ValueError(
                    "La valeur commandée ne correspond pas à la valeur"
                )

    def get_orders(
        self,
        status: str | None = None,
        ingredient_id: str | None = None,
        page: int = 1,
        limit: int = 10,
    ) -> dict[str, Any]:
        # Récupère la liste des commandes avec filtres et pagination
        try:
            query = self.client.table("orders").select(
                "*, ingredients(*)",
                count="exact",  # type: ignore
            )

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
                raise Exception("Aucune réponse de la base de données")
                
            if isinstance(response, str):
                raise Exception(f"Erreur de requête: {response}")

            if not hasattr(response, "data") or not hasattr(response, "count"):
                raise Exception("Réponse invalide de la base de données")

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
                }
            }
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des commandes: {str(e)}")

    def create_order(self, order_data: dict[str, Any]) -> dict[str, Any]:
        # Crée une nouvelle commande d'ingrédient
        try:
            # Validation des règles métier
            self.validate_order_business_rules(order_data)

            now = datetime.now(timezone.utc).isoformat()

            # Préparation des données de la commande
            order_dict = order_data.copy()
            order_dict.update({"created_at": now, "delete": False})

            # Insertion de la commande
            order_response = (
                self.client.table("orders").insert(order_dict).execute()
            )

            # Vérification que la réponse a l'attribut data
            if not order_response:
                raise Exception("Aucune réponse de la base de données")
                
            if isinstance(order_response, str):
                raise Exception(f"Erreur de requête: {order_response}")

            if not hasattr(order_response, "data") or not order_response.data:
                raise Exception("Échec de l'insertion de la commande")

            # Récupération de la commande créée
            result = order_response.data[0]
            if not isinstance(result, dict):
                raise Exception("Format de réponse invalide")
            return result

        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erreur lors de la création de la commande: {str(e)}")

    def get_order_by_id(self, order_id: int) -> dict[str, Any]:
        # Récupère une commande par son ID avec l'ingrédient
        try:
            response = (
                self.client.table("orders")
                .select("*, ingredients(*)")
                .eq("id", order_id)
                .eq("delete", False)
                .single()  
                .execute()
            )
            
            # Vérification que response.data est bien un dict
            if not response.data:
                raise Exception("Commande non trouvée")
            
            if not isinstance(response.data, dict):
                raise Exception("Format de réponse invalide")
            
            return response.data
            
        except Exception as e:
            if "0 rows" in str(e) or "not found" in str(e).lower() or "non trouvée" in str(e):
                raise Exception("Commande non trouvée")
            raise Exception(f"Erreur lors de la récupération de la commande: {str(e)}")

    def update_order(
        self, order_id: int, update_data: dict[str, Any]
    ) -> dict[str, Any]:
        # Met à jour une commande existante
        try:
            self.get_order_by_id(order_id)

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

                if not response:
                    raise Exception("Aucune réponse de la base de données")
                    
                if isinstance(response, str):
                    raise Exception(f"Erreur de requête: {response}")

            return self.get_order_by_id(order_id)

        except Exception as e:
            if "non trouvée" in str(e):
                raise e
            raise Exception(f"Erreur lors de la mise à jour de la commande: {str(e)}")

    def soft_delete_order(self, order_id: int) -> dict[str, str]:
        # Effectue une suppression logique de la commande
        try:
            _ = self.get_order_by_id(order_id)

            # Suppression logique
            _ = (
                self.client.table("orders")
                .update({"delete": True})
                .eq("id", order_id)
                .execute()
            )

            return {"detail": f"Commande {order_id} supprimée avec succès"}

        except Exception as e:
            if "non trouvée" in str(e):
                raise e
            raise Exception(f"Erreur lors de la suppression de la commande: {str(e)}")
