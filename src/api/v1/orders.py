import json
from typing import Any
from fastapi import APIRouter, HTTPException
from src.schemas import order_schema
from src.schemas.order_schema import OrderStatusEnum
from src.services.supabase_services.order_service import OrdersService
from src.api.dependencies import order_depends
from fastapi import status as http_status

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.get("/")
def get_orders(
    page: int = 1,
    limit: int = 20,
    status: OrderStatusEnum | None = None,
    ingredient_id: str | None = None,
    orders_service: OrdersService = order_depends,
):
    # Récupère la liste des commandes avec filtres et pagination.
    try:
        result = orders_service.get_orders(
            status=status.value if status else None,
            ingredient_id=ingredient_id,
            page=page,
            limit=limit,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur serveur est survenue lors de la récupération des commandes - {e}",
        )


@router.post(
    "/",
    response_model=order_schema.ORDER,
    status_code=http_status.HTTP_201_CREATED,
)
def create_order(
    order_data: order_schema.ORDER,
    orders_service: OrdersService = order_depends,
):
    """Crée une nouvelle commande."""
    try:
        order_dict = json.loads(order_data.model_dump_json())
        order = orders_service.create_order(order_dict)
        if not order:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Commande non trouvée",
            )
        return order
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur serveur est survenue lors de la création de la commande - {e}",
        )


@router.get("/{order_id}", response_model=order_schema.ORDER)
def get_order(
    order_id: int,
    orders_service: OrdersService = order_depends,  # type: ignore
):
    """Récupère les détails d'une commande par son ID"""
    try:
        order = orders_service.get_order_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Commande non trouvée",
            )
        return order
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur serveur est survenue - {e}",
        )


@router.put("/{order_id}", response_model=order_schema.ORDER)
def update_order(
    order_id: int,
    update_data: dict[str, Any],
    orders_service: OrdersService = order_depends,
):
    """Met à jour une commande existante."""
    try:
        order = orders_service.update_order(order_id, update_data)
        if not order:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Commande non trouvée",
            )
        return order
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur: {str(e)}",
        )


@router.delete(
    "/{order_id}",
    response_model=order_schema.ORDER | None,
)
def delete_order(
    order_id: int,
    orders_service: OrdersService = order_depends,  # type: ignore
):
    """Suppression logique d'une commande (soft delete)"""
    try:
        order = orders_service.soft_delete_order(order_id)
        if not order:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Commande non trouvée",
            )
        return order
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur serveur est survenue lors de la suppression - {e}",
        )
