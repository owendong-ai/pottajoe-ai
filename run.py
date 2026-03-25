import random

class PottaJoeAI:
    def __init__(self):
        # 你的商品清單
        self.products = {
            "黃金曼特寧": "風味：草本、巧克力、醇厚。適合：想提神、喜歡濃郁口感的人。",
            "衣索比亞 耶加雪菲": "風味：花香、檸檬、柑橘。適合：喜歡清爽、像茶一樣口感的人。",
            "哥倫比亞 聖奧古斯丁": "風味：焦糖、堅果。適合：初學者，口感平衡。"
        }

    def recommend_by_vibe(self, user_mood):
        """根據使用者的感覺 (Vibe) 推薦咖啡"""
        # 這裡未來可以對接真正的 AI API (如 OpenAI/Gemini)
        # 目前先用邏輯模擬 AI 的判斷
        if "累" in user_mood or "工作" in user_mood:
            choice = "黃金曼特寧"
        elif "放鬆" in user_mood or "下午茶" in user_mood:
            choice = "衣索比亞 耶加雪菲"
        else:
            choice = "哥倫比亞 聖奧古斯丁"
            
        return f"【PottaJoe AI 推薦】\n根據你現在的感覺 '{user_mood}'，最適合你的是：{choice}。\n{self.products[choice]}"

# 執行看看
ai_barista = PottaJoeAI()
print("--- 歡迎來到 PottaJoe Pour-Over Coffee AI 助手 ---")
mood = input("請問你現在的感覺如何？(例如：工作好累、想放鬆、想喝酸的): ")
print(ai_barista.recommend_by_vibe(mood))