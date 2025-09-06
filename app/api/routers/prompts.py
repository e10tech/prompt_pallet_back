from fastapi import APIRouter, Query
from app.db.supabase import supabase
from app.schemas.prompt import PromptPublic
from typing import List, Optional

router = APIRouter()


@router.get("/prompts", response_model=List[PromptPublic])
def get_public_prompts(
    category_id: Optional[int] = Query(None),
    subcategory_id: Optional[int] = Query(None),
):
    # 修正箇所: "prompts" から "public_prompts" に戻す
    query = supabase.from_("public_prompts").select("*")
    if category_id:
        query = query.eq("category_id", category_id)
    if subcategory_id:
        query = query.eq("subcategory_id", subcategory_id)

    response = query.execute()
    return response.data
