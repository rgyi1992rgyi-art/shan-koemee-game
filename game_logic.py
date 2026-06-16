from database import get_player_balance, update_player_balance

def process_game_result(user_id, bet_amount, is_winner):
    """
    user_id: ကစားသမား ID
    bet_amount: လောင်းထားတဲ့ ပိုက်ဆံပမာဏ
    is_winner: နိုင်ရင် True, ရှုံးရင် False
    """
    # ၁။ လက်ရှိ ပိုက်ဆံကို အရင်ယူမယ်
    current_balance = get_player_balance(user_id)
    
    if current_balance is None:
        return "Error: Player not found"

    # ၂။ နိုင်/ရှုံးပေါ် မူတည်ပြီး ပိုက်ဆံတွက်မယ်
    if is_winner:
        new_balance = current_balance + bet_amount
    else:
        new_balance = current_balance - bet_amount
    
    # ၃။ Database ထဲမှာ ပိုက်ဆံအသစ်ကို Update လုပ်မယ်
    update_player_balance(user_id, new_balance)
    
    return f"Success: Balance updated to {new_balance}"

# စမ်းသပ်ကြည့်ရန်
print(process_game_result("USER_001", 500, True)) # Player 1 နိုင်တယ်လို့ စမ်းကြည့်မယ်