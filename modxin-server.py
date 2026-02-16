from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 【重要】CORS設定：PyScript（ブラウザ）からの通信を許可する
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # テスト用。どこからのアクセスでも許可
    allow_methods=["*"],
    allow_headers=["*"],
)

# 受け取る指令のデータ形式を定義
class Command(BaseModel):
    instruction: str
    target_id: int

# "/api/command" というURLで指令を待ち受ける
@app.post("/api/command")
def receive_command(cmd: Command):
    # ==========================================
    # ここに、実際に動かしたいPythonの処理を書く！
    # 例：モーターを回す、DBを書き換える、スクレイピングを開始するなど
    # ==========================================
    
    print(f"💻 指令を受信しました！ 動作: {cmd.instruction}, 対象ID: {cmd.target_id}")
    
    # PyScript側に「完了したよ」という返事を返す
    return {
        "status": "success", 
        "message": f"「{cmd.instruction}」の処理が完了しました！"
    }
