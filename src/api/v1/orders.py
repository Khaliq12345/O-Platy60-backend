from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi import status as http_status
from src.schemas import order_schema
from src.services.supabase_services.order_service import OrdersService


# Définir les énums
class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


def get_orders_service() -> OrdersService:
    # Dependency pour obtenir une instance du service Orders
    return OrdersService()


@router.get("/", response_model=order_schema.OrderListResponse)
def get_orders(
    status: OrderStatusEnum | None = Query(None, description="Filtrer par statut"),  # type: ignore
    ingredient_id: str | None = Query(None, description="Filtrer par ingredient"),  # type: ignore
    page: int = Query(1, ge=1, description="Numéro de page"),  # type: ignore
    limit: int = Query(10, ge=1, le=100, description="Nombre d'éléments par page"),  # type: ignore
    orders_service: OrdersService = Depends(get_orders_service)  # type: ignore
):
    # Récupère la liste des commandes avec filtres et pagination.

    try:
        # Validation des valeurs de filtres
        valid_status = orders_service._validate_filter_values(status.value if status else None)
        
        filters = order_schema.OrderFilter(
            status=valid_status,  # type: ignore
            ingredient_id=ingredient_id,
            page=page,
            limit=limit
        )
        return orders_service.get_orders(filters)
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Paramètre invalide: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Une erreur serveur est survenue lors de la récupération des commandes"
        )


@router.post("/", response_model=order_schema.OrderWithIngredientResponse, status_code=http_status.HTTP_201_CREATED)
def create_order(
    order_data: order_schema.OrderCreate,
    orders_service: OrdersService = Depends(get_orders_service)  # type: ignore
):
    # Crée une nouvelle commande.
    try:
        return orders_service.create_order(order_data)
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Données invalides: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur serveur est survenue lors de la création de la commande"
        )


@router.get("/ingredients", response_model=list[order_schema.IngredientResponse])
def get_ingredients(
    orders_service: OrdersService = Depends(get_orders_service)  # type: ignore
):
    # Récupère la liste des ingrédients disponibles
    try:
        return orders_service.get_ingredients()
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des ingrédients"
        )


@router.get("/{order_id}", response_model=order_schema.OrderWithIngredientResponse)
def get_order(
    order_id: int,
    orders_service: OrdersService = Depends(get_orders_service)  # type: ignore
):
    # Récupère les détails d'une commande par son ID.

    try:
        return orders_service.get_order_by_id(order_id)
    except Exception as e:
        if "non trouvée" in str(e):
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND, 
                detail="Commande non trouvée"
            )
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Une erreur serveur est survenue"
        )


@router.put("/{order_id}", response_model=order_schema.OrderWithIngredientResponse)
def update_order(
    order_id: int,
    update_data: order_schema.OrderUpdate,
    orders_service: OrdersService = Depends(get_orders_service)  # type: ignore
):
    # Met à jour une commande existante.
    try:
        return orders_service.update_order(order_id, update_data)
    except Exception as e:
        if "non trouvée" in str(e):
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND, 
                detail="Commande non trouvée"
            )
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Erreur: {str(e)}"
        )


@router.delete("/{order_id}", status_code=http_status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    orders_service: OrdersService = Depends(get_orders_service)  # type: ignore
):
    # Suppression logique d'une commande (soft delete).

    try:
        orders_service.soft_delete_order(order_id)
    except Exception as e:
        if "non trouvée" in str(e):
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND, 
                detail="Commande non trouvée"
            )
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Une erreur serveur est survenue lors de la suppression"
        )


@router.post("/{order_id}/adjust", response_model=order_schema.OrderWithIngredientResponse)
def adjust_order_stock(
    order_id: int,
    adjustments: order_schema.StockAdjustmentRequest,
    orders_service: OrdersService = Depends(get_orders_service)  # type: ignore
):
    # Ajustement rapide du stock d'une commande.
    
    try:
        return orders_service.adjust_stock(order_id, adjustments)
    except Exception as e:
        if "non trouvé" in str(e):
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND, 
                detail="Commande ou item non trouvé"
            )
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Une erreur serveur est survenue lors de l'ajustement"
        )