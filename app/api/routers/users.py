from fastapi import APIRouter, Depends, HTTPException
from app.db.supabase import supabase
from app.api.deps import get_current_user
from app.schemas.prompt import UserPrompt, UserPromptCreate
from typing import List
from gotrue.types import User

router = APIRouter()


@router.get("/me/prompts", response_model=List[UserPrompt])
def get_my_prompts(current_user: User = Depends(get_current_user)):
    # RLSが効いているため、user_idで絞り込まなくても自分のデータしか返らない
    response = (
        supabase.table("user_prompt")
        .select("*")
        .eq("user_id", str(current_user.id))
        .order("created_at", desc=True)
        .execute()
    )
    return response.data


@router.post("/me/prompts", response_model=UserPrompt, status_code=201)
def create_my_prompt(
    prompt: UserPromptCreate, current_user: User = Depends(get_current_user)
):
    prompt_data = prompt.dict()
    prompt_data["user_id"] = str(current_user.id)

    response = supabase.table("user_prompt").insert(prompt_data).execute()

    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create prompt")

    return response.data[0]
