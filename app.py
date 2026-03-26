from unittest import result

from coffee_data import coffees

def recommend_coffee_by_flavor(user_flavor, excluded_names=None):
    if excluded_names is None:
        excluded_names = []

    matched = []
    for coffee in coffees:
        if coffee["flavor"] == user_flavor and coffee["name"] not in excluded_names:
            matched.append(coffee)

    if matched:
        return matched[0]

    return None


def calculate_coffee_score(coffee, preferences, recent_feedback=None, excluded_names=None):
    score = 0
    reasons = []

    if coffee["flavor"] in preferences:
        score += 3
        reasons.append(f"符合你喜歡的「{coffee['flavor']}」")

    if recent_feedback:
        score += 1
        reasons.append("根據你最近的選擇調整")

    return score, reasons   # ⭐⭐⭐ 重點在這

def get_recommend_reason(coffee, preferences, recent_feedback):
    flavor = coffee["flavor"]

    base_score = preferences.get(flavor, 0)

    liked = sum(1 for f in recent_feedback if f["flavor"] == flavor and f["feedback"] == "喜歡")
    disliked = sum(1 for f in recent_feedback if f["flavor"] == flavor and f["feedback"] == "不喜歡")

    if liked > 0:
        return f"因為你最近喜歡「{flavor}」風味 👍"

    if disliked > 0:
        return f"雖然你最近不太喜歡「{flavor}」，但仍為你提供其他選擇"

    if base_score >= 5:
        return f"你對「{flavor}」偏好很高（分數：{base_score}）"

    return f"推薦你嘗試「{flavor}」風味"

def recommend_coffee(coffees, preferences, recent_feedback, excluded_names):
    scored_coffees = []

    for coffee in coffees:
        score, reasons = calculate_coffee_score(
            coffee,
            preferences,
            recent_feedback=recent_feedback,
            excluded_names=excluded_names
        )

        scored_coffees.append((coffee, score, reasons))

    # 排序（很重要🔥）
    scored_coffees.sort(key=lambda x: x[1], reverse=True)

    results = []

    for coffee, score, reasons in scored_coffees:
        if coffee["name"] not in excluded_names:
            coffee_copy = coffee.copy()
            coffee_copy["reason"] = reasons
            results.append(coffee_copy)

    return results[:3]   # ✅ 一定要在這裡


def update_preferences(preferences, flavor, feedback):
    if feedback == "喜歡":
        preferences[flavor] += 1
    elif feedback == "不喜歡":
        preferences[flavor] -= 1