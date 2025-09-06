from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from app.schemas.prompt import Category, Subcategory
from typing import List

router = APIRouter()


@router.get("/categories", response_model=List[Category])
def get_categories():
    response = supabase.table("categories").select("*").order("id").execute()
    return response.data


@router.get("/subcategories", response_model=List[Subcategory])
def get_subcategories(category_id: int):
    response = (
        supabase.table("subcategories")
        .select("*")
        .eq("category_id", category_id)
        .order("id")
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=404, detail="Subcategories not found for the given category"
        )
    return response.data
