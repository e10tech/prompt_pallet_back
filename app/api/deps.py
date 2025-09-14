from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.db.supabase import supabase
from app.core.config import settings

# HTTPBearerは "Authorization: Bearer <token>" を解析するクラス
reusable_oauth2 = HTTPBearer(scheme_name="Bearer")


def get_current_user(token: str = Depends(reusable_oauth2)):
    try:
        # Supabaseにトークンを渡し、ユーザー情報を検証・取得
        user_response = supabase.auth.get_user(token.credentials)
        user = user_response.user
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# 新しく追加
def get_supabase_client_as_user(token: str = Depends(reusable_oauth2)):
    """
    リクエストごとに、そのユーザーのJWTで認証されたSupabaseクライアントを返す
    """
    # ここでは例としてsupabase-pyの内部的な処理を模倣しますが、
    # 実際にはリクエストヘッダーを直接PostgRESTに渡すのがよりクリーンです。
    # ここでは、JWTを渡すという概念を重視します。
    # supabase-py v2では、リクエストごとにヘッダーをオーバーライドできます。
    # この依存関係は、supabaseクライアントそのものではなく、ヘッダーを返すのが良いかもしれません。
    return {
        "Authorization": f"Bearer {token.credentials}",
        "apikey": settings.SUPABASE_KEY,  # anon key
    }
