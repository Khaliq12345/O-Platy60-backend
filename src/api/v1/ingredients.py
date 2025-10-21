import json
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from src.services.supabase_services.ingredient_service import IngredientService
from src.schemas.ingredients_schema import Ingredient
from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, Optional

router = APIRouter(prefix="/api/v1/ingredients", tags=["Ingredients"])


# GET /ingredients
@router.get("/", response_model=list[Ingredient])
def get_ingredients(
    skip: int,
    limit: int,
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
    sku: str,
    service: IngredientService = Depends(IngredientService),
):
    """Détails d’un ingrédient"""
    try:
        ingredient = service.get_ingredient(sku)
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return ingredient
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# POST /ingredients
@router.post("/", response_model=Optional[Ingredient])
def create_ingredient(
    ingredient_data: Ingredient,
    service: IngredientService = Depends(IngredientService),
):
    """Créer un nouvel ingrédient"""
    try:
        # Préparer les données pour Supabase
        data = json.loads(ingredient_data.model_dump_json())
        data["value"] = data["current_stock_level"] * data["unit_cost"]
        created = service.create_ingredient(data)

        if not created:
            raise HTTPException(status_code=401, detail="Failed to create ingredient")
        return created
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# PUT /ingredients/{sku}
@router.put("/{sku}", response_model=Optional[Ingredient])
def update_ingredient(
    sku: str,
    ingredient_data: Dict[str, Any],
    service: IngredientService = Depends(IngredientService),
):
    """Mettre à jour un ingrédient"""
    try:
        updated = service.update_ingredient(sku, ingredient_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return updated
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# DELETE /ingredients/{sku}
@router.delete("/{sku}", response_model=Optional[Ingredient])
def delete_ingredient(
    sku: str,
    service: IngredientService = Depends(IngredientService),
):
    """Suppression logique (delete=True)"""
    try:
        deleted = service.delete_ingredient(sku)
        if not deleted:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return deleted
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


@router.post("/{sku}/adjust", response_model=Optional[Ingredient])
def adjust_stock(
    sku: str,
    adjustment: float,
    service: IngredientService = Depends(IngredientService),
):
    """Ajustement rapide du stock"""
    try:
        adjusted = service.adjust_stock(sku, adjustment)
        if not adjusted:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return adjusted
    except HTTPException as e:
        raise e
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
