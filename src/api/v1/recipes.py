import json
from typing import Any, List
from fastapi import APIRouter, HTTPException
from src.schemas import recipe_schema
from src.api.dependencies import recipe_depends
from fastapi import status as http_status
from src.services.supabase_services.recipe_service import RecipeService

router = APIRouter(prefix="/api/v1/recipes", tags=["Recipes"])


@router.get("/")
def get_recipes(
    search_query: str | None = None,
    active: bool | str = "all",
    category: str | None = None,
    page: int = 1,
    limit: int = 20,
    recipe_service: RecipeService = recipe_depends,
):
    """Récupère la liste des repats avec filtres et pagination"""
    # try:
    result = recipe_service.get_recipes(
        active=active,
        search_query=search_query,
        category=category,
        page=page,
        limit=limit,
    )
    return result
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"Une erreur serveur est survenue lors de la récupération des recipes - {e}",
    #     )


@router.get(
    "/ingredients/{recipe_id}",
)
def get_recipe_ingredients(
    recipe_id: int,
    recipes_service: RecipeService = recipe_depends,  # type: ignore
):
    """Récupère les ingredients d'un repat"""
    try:
        recipe = recipes_service.get_ingredients_of_recipe(recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="repat non trouvée",
            )
        return recipe
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur serveur est survenue lors de la récupèration des ingredients - {e}",
        )


@router.post(
    "/",
    response_model=recipe_schema.Recipe,
    status_code=http_status.HTTP_201_CREATED,
)
def create_recipe(
    recipe_data: recipe_schema.Recipe,
    recipes_service: RecipeService = recipe_depends,
):
    """Crée un nouvelle repat."""
    try:
        recipe_dict = json.loads(recipe_data.model_dump_json())
        recipe = recipes_service.create_recipe(recipe_dict)
        if not recipe:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="repat non trouvée",
            )
        return recipe
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur serveur est survenue lors de la création de la repat - {e}",
        )


@router.get("/{recipe_id}", response_model=recipe_schema.Recipe)
def get_recipe(
    recipe_id: int,
    recipes_service: RecipeService = recipe_depends,  # type: ignore
):
    """Récupère les détails d'un repat par son ID"""
    try:
        recipe = recipes_service.get_recipe_by_id(recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="repat non trouvée",
            )
        return recipe
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur serveur est survenue - {e}",
        )


@router.put("/{recipe_id}", response_model=recipe_schema.Recipe)
def update_recipe(
    recipe_id: int,
    update_data: dict[str, Any],
    recipes_service: RecipeService = recipe_depends,
):
    """Met à jour un repat existante."""
    try:
        recipe = recipes_service.update_recipe(recipe_id, update_data)
        if not recipe:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="repat non trouvée",
            )
        return recipe
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur: {str(e)}",
        )


@router.delete(
    "/{recipe_id}",
    response_model=recipe_schema.Recipe,
)
def delete_recipe(
    recipe_id: int,
    recipes_service: RecipeService = recipe_depends,  # type: ignore
):
    """Suppression logique d'un repat (soft delete)"""
    try:
        recipe = recipes_service.soft_delete_recipe(recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="repat non trouvée",
            )
        return recipe
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Une erreur serveur est survenue lors de la suppression - {e}",
        )
