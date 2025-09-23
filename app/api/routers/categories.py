from fastapi import APIRouter
from app.db.supabase import supabase
from app.schemas.prompt import Category, Subcategory
from typing import List, Optional  # 1. Optional をインポート

router = APIRouter()


@router.get("/categories", response_model=List[Category])
def get_categories():
    response = supabase.table("categories").select("*").order("id").execute()
    return response.data


@router.get("/subcategories", response_model=List[Subcategory])
# 2. category_id を Optional に変更し、デフォルト値を None に設定
def get_subcategories(category_id: Optional[int] = None):
    # 3. ベースとなるクエリを作成
    query = supabase.table("subcategories").select("*")

    # 4. もし category_id が指定されていたら、絞り込み条件を追加
    if category_id is not None:
        query = query.eq("category_id", category_id)

    # 常にidでソートして実行
    response = query.order("id").execute()

    # 5. HTTPExceptionを削除。データがなくても空のリスト[]を返すのが自然
    return response.data
