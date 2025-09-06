from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import categories, prompts, users

# FastAPIインスタンスを作成
app = FastAPI(title="Prompt Pallet API")

# CORS (Cross-Origin Resource Sharing) の設定
# フロントエンド (Next.js) からのアクセスを許可する
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],  # Next.jsの開発サーバのURL
    allow_origins=[
        "https://prompt-pallet-kappa.vercel.app"
    ],  # 本番環境では適切なオリジンを指定することを推奨
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターを登録
# /api/v1 というプレフィックスをつける
api_prefix = "/api/v1"
app.include_router(categories.router, prefix=api_prefix, tags=["Categories"])
app.include_router(prompts.router, prefix=api_prefix, tags=["Prompts"])
app.include_router(users.router, prefix=api_prefix, tags=["Users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Prompt Pallet API"}
