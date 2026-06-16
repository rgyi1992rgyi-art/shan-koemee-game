import os
from supabase import create_client

# Railway ထဲမှာ ထည့်ထားမယ့် နာမည်တွေကို ခေါ်သုံးတာပါ
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_player_balance(user_id):
    """ကစားသမားရဲ့ လက်ရှိပိုက်ဆံကို Fetch လုပ်ရန်"""
    response = supabase.table("players").select("balance").eq("user_id", user_id).single().execute()
    if response.data:
        return response.data['balance']
    return None

def update_player_balance(user_id, new_balance):
    """ပွဲပြီးရင် ပိုက်ဆံအသစ်ကို Update လုပ်ရန်"""
    response = supabase.table("players").update({"balance": new_balance}).eq("user_id", user_id).execute()
    return response

# စမ်းသပ်ကြည့်ရန်
if __name__ == "__main__":
    balance = get_player_balance("USER_001")
    print(f"Player 1 ၏ လက်ကျန်ငွေ: {balance}")