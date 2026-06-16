from database import supabase

def test_connection():
    try:
        # players table ထဲက data တွေကို လှမ်းဖတ်ကြည့်မယ်
        response = supabase.table("players").select("*").execute()
        print("✅ ချိတ်ဆက်မှု အောင်မြင်ပါတယ်!")
        print("Database ထဲက အချက်အလက်များ -", response.data)
    except Exception as e:
        print("❌ ချိတ်ဆက်မှု မအောင်မြင်ပါ")
        print("Error အကြောင်းရင်း -", e)

if __name__ == "__main__":
    test_connection()