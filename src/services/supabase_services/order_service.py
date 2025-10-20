# order_service.py

from src.services.supabase_services.supabase_service import SupabaseService
from src.schemas import order_schema
from typing import Any
from datetime import datetime, timezone


class OrdersService(SupabaseService):
    orders_table: str
    ingredients_table: str

    def __init__(self) -> None:
        super().__init__()
        self.orders_table = "orders"
        self.ingredients_table = "ingredients"

    def _validate_order_business_rules(
        self, order_data: order_schema.OrderCreate
    ) -> None:
        # Valide les règles métier d'une commande
        # Vérifier que la quantité commandée est positive
        if order_data.quantity_ordered <= 0:
            raise ValueError("La quantité commandée doit être positive")

        # Vérifier que le prix unitaire est positif
        if order_data.unit_price_ordered < 0:
            raise ValueError("Le prix unitaire commandé ne peut pas être négatif")

        # Vérifier que la valeur commandée est cohérente
        if order_data.value_ordered < 0:
            raise ValueError("La valeur commandée ne peut pas être négative")

        # Vérifier la cohérence entre quantité, prix unitaire et valeur
        expected_value = order_data.quantity_ordered * order_data.unit_price_ordered
        if (
            abs(order_data.value_ordered - expected_value) > 0.01
        ):  # Tolérance pour les arrondis
            raise ValueError(
                "La valeur commandée ne correspond pas à quantité × prix unitaire"
            )

    def _validate_filter_values(self, status: str | None) -> str | None:
        # Valide les valeurs de filtres pour s'assurer qu'elles correspondent aux types
        valid_status = None

        if status:
            if status in ["pending", "confirmed", "completed", "cancelled"]:
                valid_status = status
            else:
                raise ValueError(
                    f"Status invalide: {status}. Valeurs autorisées: pending, confirmed, completed, cancelled"
                )

        return valid_status

    def get_orders(self, filters: order_schema.OrderFilter) -> dict[str, Any]:
        # Récupère la liste des commandes avec filtres et pagination
        try:
            query = self.client.table(self.orders_table).select(
                "*, ingredients(*)",
                count="exact",  # type: ignore
            )

            # Application des filtres
            query = query.eq("delete", filters.delete)

            if filters.status:
                query = query.eq("status", filters.status)

            if filters.ingredient_id:
                query = query.eq("ingredient_id", filters.ingredient_id)

            # Calcul de l'offset pour la pagination
            offset = (filters.page - 1) * filters.limit

            # Exécution de la requête unique avec pagination
            response = query.range(offset, offset + filters.limit - 1).execute()

            # Vérification de la réponse
            if isinstance(response, str):
                raise Exception(f"Erreur de requête: {response}")

            if not hasattr(response, "data") or not hasattr(response, "count"):
                raise Exception("Réponse invalide de la base de données")

            # On s'assure que 'total' est un entier pour éviter une erreur de type plus loin
            total = response.count if response.count is not None else 0

            return {
                "orders": response.data,
                "total": total,
                "page": filters.page,
                "limit": filters.limit,
                "has_next": offset + filters.limit < total,
                "has_prev": filters.page > 1,
            }
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des commandes: {str(e)}")

    def create_order(self, order_data: order_schema.OrderCreate) -> dict[str, Any]:
        # Crée une nouvelle commande d'ingrédient
        try:
            # Validation des règles métier
            self._validate_order_business_rules(order_data)

            now = datetime.now(timezone.utc).isoformat()

            # Préparation des données de la commande
            order_dict = order_data.model_dump()
            order_dict.update({"created_at": now, "delete": False})

            # Insertion de la commande
            order_response = (
                self.client.table(self.orders_table).insert(order_dict).execute()
            )

            # Vérification que la réponse a l'attribut data
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
                self.client.table(self.orders_table)
                .select("*, ingredients(*)")
                .eq("id", order_id)
                .eq("delete", False)
                .execute()
            )

            # Vérification que la réponse a l'attribut data
            if isinstance(response, str):
                raise Exception(f"Erreur de requête: {response}")

            if not hasattr(response, "data") or not response.data:
                raise Exception("Commande non trouvée")

            result = response.data[0]
            if not isinstance(result, dict):
                raise Exception("Format de réponse invalide")
            return result

        except Exception as e:
            if "non trouvée" in str(e):
                raise e
            raise Exception(f"Erreur lors de la récupération de la commande: {str(e)}")

    def update_order(
        self, order_id: int, update_data: order_schema.OrderUpdate
    ) -> dict[str, Any]:
        # Met à jour une commande existante
        try:
            _ = self.get_order_by_id(order_id)

            # Préparation des données de mise à jour (exclusion des valeurs None)
            update_dict = update_data.model_dump(exclude_unset=True)

            if update_dict:
                response = (
                    self.client.table(self.orders_table)
                    .update(update_dict)
                    .eq("id", order_id)
                    .execute()
                )

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
                self.client.table(self.orders_table)
                .update({"delete": True})
                .eq("id", order_id)
                .execute()
            )

            return {"detail": f"Commande {order_id} supprimée avec succès"}

        except Exception as e:
            if "non trouvée" in str(e):
                raise e
            raise Exception(f"Erreur lors de la suppression de la commande: {str(e)}")

    def adjust_stock(
        self, order_id: int, adjustments: order_schema.StockAdjustmentRequest
    ) -> dict[str, Any]:
        # Ajuste les quantités/prix reçus d'une commande
        try:
            _ = self.get_order_by_id(order_id)

            # Application des ajustements
            for adjustment in adjustments.adjustments:
                # Vérifier que l'adjustment concerne bien cette commande
                if adjustment.order_id != order_id:
                    raise ValueError(
                        f"L'ajustement ne concerne pas la commande {order_id}"
                    )

                # Calcul de la nouvelle valeur reçue
                new_value_received = (
                    adjustment.new_quantity_received
                    * adjustment.new_unit_price_received
                )

                # Mise à jour de la commande
                update_data: dict[str, Any] = {
                    "quantity_received": adjustment.new_quantity_received,
                    "unit_price_received": adjustment.new_unit_price_received,
                    "value_received": new_value_received,
                }

                # Ajouter la raison dans les notes
                if adjustment.reason:
                    current_order = self.get_order_by_id(order_id)
                    current_notes = current_order.get("notes", "")
                    if isinstance(current_notes, str):
                        update_data["notes"] = (
                            f"{current_notes}\nAjustement: {adjustment.reason}"
                            if current_notes
                            else f"Ajustement: {adjustment.reason}"
                        )
                    else:
                        update_data["notes"] = f"Ajustement: {adjustment.reason}"

                _ = (
                    self.client.table(self.orders_table)
                    .update(update_data)
                    .eq("id", order_id)
                    .execute()
                )

            # Récupération de la commande mise à jour
            return self.get_order_by_id(order_id)

        except Exception as e:
            if "non trouvée" in str(e) or "non trouvé" in str(e):
                raise e
            raise Exception(f"Erreur lors de l'ajustement du stock: {str(e)}")

    def get_ingredients(self) -> list[dict[str, Any]]:
        # Récupère la liste des ingrédients
        try:
            response = (
                self.client.table(self.ingredients_table)
                .select("*")
                .eq("delete", False)
                .execute()
            )

            if isinstance(response, str):
                raise Exception(f"Erreur de requête: {response}")

            if not hasattr(response, "data"):
                raise Exception("Réponse invalide de la base de données")

            data = response.data
            if not isinstance(data, list):
                return []

            # Cast de la réponse JSON en list
            result: list[dict[str, Any]] = []
            for item in data:
                if isinstance(item, dict):
                    result.append(item)
            return result

        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des ingrédients: {str(e)}")
