import json
from fastapi import APIRouter, HTTPException, Depends, Path
from src.schemas.ingredients_schema import Ingredient
from src.api.dependencies import ingredient_depends
from src.services.supabase_services.ingredient_service import IngredientService
from typing import Any, Dict, Optional, List

router = APIRouter(prefix="/api/v1/ingredients", tags=["Ingredients"])


# GET /ingredients
@router.get("/", response_model=List[Ingredient])
def get_ingredients(
    skip: int = 0,
    limit: int = 10,
    service: IngredientService = ingredient_depends,
):
    """Liste des ingrédients avec delete=False et pagination Supabase"""
    try:
        return service.get_ingredients(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# GET /ingredients/{sku}
@router.get("/{sku}", response_model=Ingredient)
def get_ingredient(
    sku: str,
    service: IngredientService = ingredient_depends,
):
    """Détails d’un ingrédient"""
    try:
        ingredient = service.get_ingredient(sku)
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return ingredient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# POST /ingredients
@router.post("/", response_model=Optional[Ingredient])
def create_ingredient(
    ingredient_data: Ingredient,
    service: IngredientService = ingredient_depends,
):
    """Créer un nouvel ingrédient"""
    try:
        data = json.loads(ingredient_data.model_dump_json())
        data["value"] = data["current_stock_level"] * data["unit_cost"]
        created = service.create_ingredient(data)

        if not created:
            raise HTTPException(status_code=400, detail="Failed to create ingredient")
        return created
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# PUT /ingredients/{sku}
@router.put("/{sku}", response_model=Optional[Ingredient])
def update_ingredient(
    sku: str,
    ingredient_data: Dict[str, Any],
    service: IngredientService = ingredient_depends,
):
    """Mettre à jour un ingrédient"""
    try:
        updated = service.update_ingredient(sku, ingredient_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# DELETE /ingredients/{sku}
@router.delete("/{sku}", response_model=Optional[Ingredient])
def delete_ingredient(
    sku: str,
    service: IngredientService = ingredient_depends,
):
    """Suppression logique (delete=True)"""
    try:
        deleted = service.delete_ingredient(sku)
        if not deleted:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return deleted
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# POST /ingredients/{sku}/adjust
@router.post("/{sku}/adjust", response_model=Optional[Ingredient])
def adjust_stock(
    sku: str,
    adjustment: float,
    service: IngredientService = ingredient_depends,
):
    """Ajustement rapide du stock"""
    try:
        adjusted = service.adjust_stock(sku, adjustment)
        if not adjusted:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return adjusted
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# GET /ingredients/{sku}/history
@router.get("/{sku}/history")
def get_history(
    sku: str = Path(...),
    service: IngredientService = ingredient_depends,
):
    """Historique des mouvements (placeholder)"""
    try:
        return service.get_history(sku)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# GET /ingredients/{sku}/batches
@router.get("/{sku}/batches")
def get_batches(
    sku: str = Path(...),
    service: IngredientService = ingredient_depends,
):
    """Lots groupés par date d’expiration (placeholder)"""
    try:
        return service.get_batches(sku)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")
