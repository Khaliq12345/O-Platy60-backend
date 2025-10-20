from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from src.schemas import order_schema
from src.api.dependencies import get_orders_service, orders_depends
from src.services.supabase_services.order_service import OrdersService
from typing import Any 


# Définir les énums
class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.get("/")
def get_orders(
    status: OrderStatusEnum | None = Query(None, description="Filtrer par statut"),
    ingredient_id: str | None = Query(None, description="Filtrer par ingredient"),
    page: int = Query(1, ge=1, description="Numéro de page"),
    limit: int = Query(10, ge=1, le=100, description="Nombre d'éléments par page"),
    orders_service: OrdersService = Depends(get_orders_service),
):
    # Récupère la liste des commandes avec filtres et pagination.
    try:
        result = orders_service.get_orders(
            status=status.value if status else None,
            ingredient_id=ingredient_id,
            page=page,
            limit=limit
        )
        
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Paramètre invalide: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur serveur est survenue lors de la récupération des commandes",
        )


@router.post("/", response_model=order_schema.ORDER, status_code=http_status.HTTP_201_CREATED)
def create_order(
    order_data: dict[str, Any],
    orders_service: OrdersService = Depends(get_orders_service),
):
    # Crée une nouvelle commande.
    try:
        return orders_service.create_order(order_data)
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Données invalides: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur serveur est survenue lors de la création de la commande",
        )


@router.get("/{order_id}", response_model=order_schema.ORDER)
def get_order(
    order_id: int,
    orders_service: OrdersService = Depends(get_orders_service),  # type: ignore
):
    # Récupère les détails d'une commande par son ID.

    try:
        return orders_service.get_order_by_id(order_id)
    except Exception as e:
        if "non trouvée" in str(e):
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Commande non trouvée",
            )
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur serveur est survenue",
        )


@router.put("/{order_id}", response_model=order_schema.ORDER)
def update_order(
    order_id: int,
    update_data: dict[str, Any],
    orders_service: OrdersService = Depends(get_orders_service),
):
    # Met à jour une commande existante.
    try:
        return orders_service.update_order(order_id, update_data)
    except Exception as e:
        if "non trouvée" in str(e):
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Commande non trouvée",
            )
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur: {str(e)}",
        )


@router.delete("/{order_id}", status_code=http_status.HTTP_204_NO_CONTENT, response_model=None)
def delete_order(
    order_id: int,
    orders_service: OrdersService = Depends(get_orders_service),  # type: ignore
):
    # Suppression logique d'une commande (soft delete).

    try:
        orders_service.soft_delete_order(order_id)
    except Exception as e:
        if "non trouvée" in str(e):
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Commande non trouvée",
            )
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur serveur est survenue lors de la suppression",
        )
