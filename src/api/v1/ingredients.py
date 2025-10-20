from fastapi import APIRouter, HTTPException, Depends, Path, Query
from typing import List
from src.services.supabase_services.ingredient_service import IngredientService
from src.schemas.ingredients_schema import Ingredient
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/v1/ingredients", tags=["Ingredients"])


# Schema pour la création (pas tous les champs obligatoires)
class IngredientCreate(BaseModel):
    sku: str
    name: str
    category: Optional[str]
    current_stock_level: float
    unit: Optional[str]
    min_stock_level: float
    storage_location: Optional[str]
    last_received: Optional[datetime]
    unit_cost: float
    expire_at: Optional[datetime]


# GET /ingredients
@router.get("/", response_model=List[Ingredient])
def get_ingredients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: IngredientService = Depends(IngredientService),
):
    """Liste des ingrédients avec delete=False et pagination Supabase"""
    try:
        ingredients = service.get_ingredients(skip=skip, limit=limit)
        return ingredients
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# GET /ingredients/{sku}
@router.get("/{sku}", response_model=Ingredient)
def get_ingredient(
    sku: str = Path(...),
    service: IngredientService = Depends(IngredientService),
):
    """Détails d’un ingrédient"""
    try:
        ingredient = service.get_ingredient(sku)
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return ingredient
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# POST /ingredients
@router.post("/", response_model=Ingredient)
def create_ingredient(
    ingredient_data: IngredientCreate,
    service: IngredientService = Depends(IngredientService),
):
    """Créer un nouvel ingrédient"""
    try:
        # Préparer les données pour Supabase
        data = ingredient_data.dict()
        data["last_updated"] = datetime.utcnow()
        data["value"] = data["current_stock_level"] * data["unit_cost"]

        # Sérialiser les dates si nécessaire (last_received, expire_at)
        for key in ["last_received", "expire_at", "last_updated"]:
            if key in data and isinstance(data[key], datetime):
                data[key] = data[key].isoformat()

        created = service.create_ingredient(data)

        if not created:
            raise HTTPException(status_code=500, detail="Failed to create ingredient")

        # Retourner un objet validé par Pydantic
        return Ingredient(**created[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# PUT /ingredients/{sku}
@router.put("/{sku}", response_model=Ingredient)
def update_ingredient(
    sku: str = Path(...),
    ingredient_data: IngredientCreate = ...,
    service: IngredientService = Depends(IngredientService),
):
    """Mettre à jour un ingrédient"""
    try:
        updated = service.update_ingredient(sku, ingredient_data.dict())
        if not updated:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# DELETE /ingredients/{sku}
@router.delete("/{sku}", response_model=Ingredient)
def delete_ingredient(
    sku: str = Path(...),
    service: IngredientService = Depends(IngredientService),
):
    """Suppression logique (delete=True)"""
    try:
        deleted = service.delete_ingredient(sku)
        if not deleted:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return deleted
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# POST /ingredients/{sku}/adjust
class StockAdjustment(BaseModel):
    quantity: float


@router.post("/{sku}/adjust", response_model=Ingredient)
def adjust_stock(
    sku: str = Path(...),
    adjustment: StockAdjustment = ...,
    service: IngredientService = Depends(IngredientService),
):
    """Ajustement rapide du stock"""
    try:
        adjusted = service.adjust_stock(sku, adjustment.quantity)
        if not adjusted:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return adjusted
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# GET /ingredients/{sku}/history
@router.get("/{sku}/history")
def get_history(
    sku: str = Path(...),
    service: IngredientService = Depends(IngredientService),
):
    """Historique des mouvements (placeholder)"""
    return service.get_history(sku)


# GET /ingredients/{sku}/batches
@router.get("/{sku}/batches")
def get_batches(
    sku: str = Path(...),
    service: IngredientService = Depends(IngredientService),
):
    """Lots groupés par date d’expiration (placeholder)"""
    return service.get_batches(sku)
