from app import recommend_coffee_by_flavor, recommend_by_preferences
from user_data import load_preferences, save_preferences

def show_menu():
    print("\n請選擇你喜歡的口味：")
    print("1. 濃郁")
    print("2. 果香")
    print("3. 堅果")
    print("4. 花香")
    print("5. 再推薦一個")
    print("6. AI 幫我推薦")
    print("0. 離開")

def map_choice_to_flavor(choice):
    mapping = {
        "1": "濃郁",
        "2": "果香",
        "3": "堅果",
        "4": "花香"
    }
    return mapping.get(choice)

def ask_rating(coffee_name):
    print("\n你覺得這款咖啡如何？")
    print("1. 喜歡")
    print("2. 不喜歡")
    print("0. 略過")

    rating = input("請輸入評價（0-2）：")

    if rating == "1":
        return "喜歡"
    elif rating == "2":
        return "不喜歡"
    else:
        return "略過"

def update_preferences(preferences, flavor, feedback):
    if feedback == "喜歡":
        preferences[flavor] = preferences.get(flavor, 0) + 1
    elif feedback == "不喜歡":
        preferences[flavor] = preferences.get(flavor, 0) - 1

def show_preferences(preferences):
    print("\n目前 AI 學到的你的偏好分數：")
    for flavor, score in preferences.items():
        print(f"{flavor}：{score}")

def main():
    print("☕ 歡迎使用 PottaJoe 咖啡推薦系統")

    last_flavor = None
    recommended_names = []
    feedback_history = []

    preferences = load_preferences()

    print("\n已載入你的偏好資料：")
    show_preferences(preferences)

    while True:
        show_menu()
        choice = input("請輸入選項（0-6）：")

        if choice == "0":
            save_preferences(preferences)

            print("\n你的評價紀錄：")
            for item in feedback_history:
                print(f'- {item["coffee"]}：{item["feedback"]}')

            print("\n偏好已儲存。")
            show_preferences(preferences)
            print("\n感謝使用 PottaJoe，再見！")
            break

        elif choice == "5":
            if last_flavor:
                result = recommend_coffee_by_flavor(last_flavor, recommended_names)
            else:
                print("請先選擇一個口味 😊")
                continue

        elif choice == "6":
            result = recommend_by_preferences(preferences, recommended_names)
            if result:
                last_flavor = result["flavor"]
            else:
                print("目前沒有可推薦的咖啡。")
                continue

        else:
            flavor = map_choice_to_flavor(choice)

            if not flavor:
                print("請輸入有效選項（0-6）")
                continue

            last_flavor = flavor
            recommended_names = []
            result = recommend_coffee_by_flavor(flavor, recommended_names)

        if result:
            recommended_names.append(result["name"])

            print("\n☕ 推薦給你的咖啡：")
            print("名稱：", result["name"])
            print("風味：", result["flavor"])
            print("介紹：", result["description"])

            feedback = ask_rating(result["name"])
            feedback_history.append({
                "coffee": result["name"],
                "feedback": feedback
            })

            update_preferences(preferences, result["flavor"], feedback)

            print(f'已記錄你對「{result["name"]}」的評價：{feedback}')
            show_preferences(preferences)

        else:
            print("\n這個口味已經推薦完了，換一個試試吧！")

        print("-" * 30)

if __name__ == "__main__":
    main()