import json
from fastapi import APIRouter, HTTPException, Path, status as http_status
from src.schemas.ingredients_schema import Ingredient, Stock_Adjustment
from src.api.dependencies import ingredient_depends
from src.services.supabase_services.ingredient_service import IngredientService
from typing import Any, Dict, Optional

router = APIRouter(prefix="/api/v1/ingredients", tags=["Ingredients"])


# GET /ingredients
@router.get("/", response_model=dict)
def get_ingredients(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    category: str | None = None,
    status: str | None = None,
    low_stock_only: bool | None = False,
    ingredient_service: IngredientService = ingredient_depends,
):
    """
    Récupère la liste des ingrédients (delete=False) avec pagination et filtres optionnels.
    """
    try:
        result = ingredient_service.get_ingredients(
            page=page,
            limit=limit,
            search=search,
            category=category,
            status=status,
            low_stock_only=low_stock_only,
        )

        if not result:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Aucun ingrédient trouvé.",
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur serveur est survenue lors de la récupération des ingrédients - {e}",
        )


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
@router.post("/adjust")
def adjust_stock(
    adjustment_data: Stock_Adjustment,
    service: IngredientService = ingredient_depends,
):
    """Ajustement rapide du stock"""
    try:
        adjustment_dict = json.loads(adjustment_data.model_dump_json())
        adjusted = service.adjust_stock(adjustment_dict)
        return adjusted
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# GET /ingredients/history/{sku}
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


# GET /ingredients/batches/{sku}
@router.get("/{sku}/batches")
def get_batches(
    sku: str,
    service: IngredientService = ingredient_depends,
):
    """Lots groupés par date d’expiration (placeholder)"""
    try:
        return service.get_batches(sku)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# SEARCH INGREDIENTS
@router.get("/search/{keyword}")
def search_ingredients(
    keyword: str,
    service: IngredientService = ingredient_depends,
):
    """Search for Ingredients"""
    try:
        searches = service.search_ingredient(keyword)
        return searches
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# GET RECIPES
@router.get("/recipes/{sku}")
def get_recipes(
    sku: str,
    service: IngredientService = ingredient_depends,
):
    """Get Recipes using this Ingredient"""
    try:
        recipes = service.get_recipes(sku)
        return recipes
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")
