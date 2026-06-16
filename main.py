from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import List
from game import Player, GameRoom
from database import DBManager # Database ကို ခေါ်သုံးရန်

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()
game_room = GameRoom()

# --- HTML FRONTEND UI ---
html_code = """
"""

@app.get("/")
def get_game_page():
    return HTMLResponse(html_code)

# --- WEBSOCKET ENDPOINT ---
@app.websocket("/ws/{user_id}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, user_name: str):
    await manager.connect(websocket)
    
    # 💡 DB မှ Player data ကို Fetch လုပ်ပြီး Player ဆောက်ခြင်း
    db_player = DBManager.get_player_balance(user_id, user_name)
    current_player = Player(
        user_id=db_player["user_id"], 
        name=db_player["name"], 
        balance=db_player["balance"]
    )
    
    game_room.add_player(current_player)
    await manager.broadcast(f"📢 {current_player.name} ဝိုင်းထဲဝင်လာပါပြီ။ (လက်ကျန်ငွေ: {current_player.balance} ကျပ်)")
    
    try:
        while True:
            data = await websocket.receive_text()
            if data == "/deal":
                status = game_room.start_new_round()
                if "⚠️" in status:
                    await websocket.send_text(status)
                else:
                    await manager.broadcast("🃏 ဖဲဝေပြီး ရလဒ်တွက်ချက်နေပါပြီ...")
                    # 💡 Database နှင့် ချိတ်ဆက်ပြီး ရလဒ်ထုတ်ခြင်း (await သုံးပါ)
                    game_result = await game_room.check_winner()
                    await manager.broadcast(game_result)
            else:
                await manager.broadcast(f"{current_player.name}: {data}")
    except Exception as e:
        manager.disconnect(websocket)
        # ထွက်သွားလျှင်လည်း DB ကို နောက်ဆုံးတစ်ကြိမ် update လုပ်ရန်လိုပါက ဤနေရာတွင် စီစဉ်နိုင်သည်
        await manager.broadcast(f"❌ {current_player.name} ထွက်သွားပါပြီ။")