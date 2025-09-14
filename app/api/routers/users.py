from fastapi import APIRouter, Depends, HTTPException
from app.db.supabase import supabase
from app.api.deps import get_current_user, get_supabase_client_as_user
from app.schemas.prompt import UserPrompt, UserPromptCreate
from typing import List
from gotrue.types import User
from supabase import create_client
from app.core.config import settings

router = APIRouter()


@router.get("/me/prompts", response_model=List[UserPrompt])
def get_my_prompts(
    # current_userはuser_idの存在確認のために残しても良い
    current_user: User = Depends(get_current_user),
    # ユーザー権限のヘッダーを取得
    user_headers: dict = Depends(get_supabase_client_as_user),
):
    # supabase-py v2の `auth()` メソッドを使って一時的にユーザーを切り替える
    # または、execute()のオプションでヘッダーを渡す
    # Supabaseクライアントを一時的にそのユーザーとして振る舞わせる
    authed_supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    authed_supabase.postgrest.auth(user_headers["Authorization"].split(" ")[1])

    # .eq("user_id", ...) を書かなくても、RLSが自動でフィルタリングしてくれる！
    response = (
        authed_supabase.table("user_prompt")
        .select("*")
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
