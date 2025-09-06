from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


# カテゴリの基本形
class Category(BaseModel):
    id: int
    name: str


# サブカテゴリの基本形
class Subcategory(BaseModel):
    id: int
    category_id: int
    name: str


# 公開プロンプトのレスポンス用
class PromptPublic(BaseModel):
    id: int
    category_id: int
    subcategory_id: int
    prompt: str
    japanese_label: str
    is_positive: bool
    owner_id: Optional[uuid.UUID] = None
    source: str


# ユーザープロンプトの作成用
class UserPromptCreate(BaseModel):
    category_id: int
    subcategory_id: int
    prompt: str
    japanese_label: str
    is_positive: bool = True
    is_public: bool = False


# ユーザープロンプトのレスポンス用
class UserPrompt(UserPromptCreate):
    id: int
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
