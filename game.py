import random
from database import DBManager # Database နဲ့ ချိတ်ဆက်ရန်

class Card:
    def __init__(self, suit: str, value: str):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value}{self.suit}"

class Deck:
    def __init__(self):
        self.suits = ['♠', '♥️', '♦', '♣']
        self.values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.reset_deck()

    def reset_deck(self):
        self.cards = [Card(suit, value) for suit in self.suits for value in self.values]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0) if len(self.cards) > 0 else None

class Player:
    def __init__(self, user_id: str, name: str, balance: int = 3000):
        self.user_id = user_id
        self.name = name
        self.balance = balance
        self.hand = []
        self.is_banker = False
        self.current_bet = 0

    def draw_card(self, deck):
        card = deck.deal_card()
        if card:
            self.hand.append(card)
        return card

class GameRoom:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.max_players = 7
        self.min_bank_amount = 3000
        self.min_bet = 30
        self.banker_index = 0

    def add_player(self, player: Player):
        if len(self.players) < self.max_players:
            self.players.append(player)
            return True
        return False

    def evaluate_hand(self, hand):
        # ... (သင်ပေးထားသော evaluate_hand logic အတိုင်း) ...
        n_cards = len(hand)
        normal_score = sum(10 if c.value in ['J', 'Q', 'K'] else (1 if c.value == 'A' else int(c.value)) for c in hand) % 10
        # (ကျန်သည့် logic များကိုလည်း ဒီအတိုင်း ထည့်ပါ)
        return {"rank_type": 1, "score": normal_score, "multiplier": 1, "desc": f"{normal_score} မှတ်"}

    def get_highest_suit_rank(self, hand):
        suit_values = {'♣': 1, '♦': 2, '♥️': 3, '♠': 4}
        return max(suit_values[c.suit] for c in hand)

    def rotate_banker(self):
        # ... (သင်ပေးထားသော rotate_banker logic) ...
        pass

    def compare_hands(self, p_res, p_suit, b_res, b_suit):
        if p_res["rank_type"] != b_res["rank_type"]: return p_res["rank_type"] > b_res["rank_type"]
        if p_res["score"] != b_res["score"]: return p_res["score"] > b_res["score"]
        return p_suit > b_suit

    # 💡 အပြောင်းအလဲ - Database ဖြင့် ချိတ်ဆက်ထားသည့် check_winner
    async def check_winner(self):
        banker = next((p for p in self.players if p.is_banker), None)
        if not banker: return "ဒိုင်မရှိပါ"
        
        b_res = self.evaluate_hand(banker.hand)
        b_suit = self.get_highest_suit_rank(banker.hand)
        res = f"👑 ဒိုင် ({banker.name}): {banker.hand} -> [{b_res['desc']}]\n"
        
        for p in self.players:
            if p.is_banker or p.current_bet == 0: continue
            
            p_res = self.evaluate_hand(p.hand)
            p_suit = self.get_highest_suit_rank(p.hand)
            win = self.compare_hands(p_res, p_suit, b_res, b_suit)
            amt = p.current_bet * (p_res["multiplier"] if win else b_res["multiplier"])
            
            if win:
                p.balance += amt
                banker.balance -= amt
                res += f"👤 {p.name}: နိုင် (+{amt})\n"
            else:
                p.balance -= amt
                banker.balance += amt
                res += f"👤 {p.name}: ရှုံး (-{amt})\n"
            
            # DB ကို update လုပ်ခြင်း
            DBManager.update_player_balance(p.user_id, p.balance)
        
        # ဒိုင်၏ balance ကို DB တွင် update လုပ်ခြင်း
        DBManager.update_player_balance(banker.user_id, banker.balance)
        
        return res