from fastapi import APIRouter, HTTPException, Depends, Path, Query
from src.services.supabase_services.ingredient_service import IngredientService

router = APIRouter(prefix="/api/v1/ingredients", tags=["Ingredients"])


# GET /ingredients
@router.get("/")
def get_ingredients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    service: IngredientService = Depends(IngredientService),
):
    """Liste des ingrédients avec delete=False et pagination"""
    try:
        ingredients = service.get_ingredients()
        return ingredients[skip : skip + limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# GET /ingredients/{sku}
@router.get("/{sku}")
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
@router.post("/")
def create_ingredient(
    ingredient_data: dict,
    service: IngredientService = Depends(IngredientService),
):
    """Créer un nouvel ingrédient"""
    try:
        return service.create_ingredient(ingredient_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# PUT /ingredients/{sku}
@router.put("/{sku}")
def update_ingredient(
    sku: str = Path(...),
    ingredient_data: dict = ...,
    service: IngredientService = Depends(IngredientService),
):
    """Mettre à jour un ingrédient"""
    try:
        updated = service.update_ingredient(sku, ingredient_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error - {e}")


# DELETE /ingredients/{sku}
@router.delete("/{sku}")
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
@router.post("/{sku}/adjust")
def adjust_stock(
    sku: str = Path(...),
    adjustment: dict = ...,
    service: IngredientService = Depends(IngredientService),
):
    """Ajustement rapide du stock (quantity dans adjustment dict)"""
    try:
        quantity = adjustment.get("quantity")
        if quantity is None:
            raise HTTPException(status_code=400, detail="Missing 'quantity'")
        adjusted = service.adjust_stock(sku, quantity)
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
