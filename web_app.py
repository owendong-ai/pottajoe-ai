from flask import Flask, render_template, request, redirect, url_for, session
from app import (get_recommend_reason, recommend_coffee,
                 recommend_coffee_by_flavor, recommend_coffee_by_roast,
                 recommend_coffees_by_flavor, recommend_coffees_by_roast,
                 recommend_top3, update_preferences)
from coffee_data import coffees
from user_data import load_preferences, save_preferences

app = Flask(__name__)
app.secret_key = "pottajoe_secret_key"


@app.route("/")
def home():
    preferences = load_preferences()

    if "recommended_names" not in session:
        session["recommended_names"] = []

    if "recent_feedback" not in session:
        session["recent_feedback"] = []

    return render_template("index.html", preferences=preferences)


@app.route("/recommend", methods=["POST"])
def recommend():
    choice = request.form.get("choice")
    preferences = load_preferences()

    if "recommended_names" not in session:
        session["recommended_names"] = []

    if "recent_feedback" not in session:
        session["recent_feedback"] = []

    recommended_names = session["recommended_names"]
    recent_feedback = session["recent_feedback"]

    flavor_map = {
        "1": "濃郁",
        "2": "果香",
        "3": "堅果",
        "4": "花香"
    }

    roast_map = {
        "7": "淺焙",
        "8": "中焙",
        "9": "深焙"
    }

    if choice in flavor_map:
        flavor = flavor_map[choice]
        session["last_flavor"] = flavor
        session["last_roast"] = None
        session["recommended_names"] = []

        results = recommend_coffees_by_flavor(flavor, [])
        if results:
            new_excluded = [c["name"] for c in results]
            session["recommended_names"] = new_excluded
            has_more = bool(recommend_coffees_by_flavor(flavor, new_excluded, limit=1))
            return render_template(
                "result.html",
                coffee=None,
                coffees=results,
                preferences=preferences,
                has_more=has_more,
                page_title=f"☕ 為你推薦的{flavor}咖啡"
            )

    elif choice in roast_map:
        roast = roast_map[choice]
        session["last_roast"] = roast
        session["last_flavor"] = None
        session["recommended_names"] = []

        results = recommend_coffees_by_roast(roast, [])
        if results:
            new_excluded = [c["name"] for c in results]
            session["recommended_names"] = new_excluded
            has_more = bool(recommend_coffees_by_roast(roast, new_excluded, limit=1))
            return render_template(
                "result.html",
                coffee=None,
                coffees=results,
                preferences=preferences,
                has_more=has_more,
                page_title=f"☕ 為你推薦的{roast}咖啡"
            )

    elif choice == "5":
        last_flavor = session.get("last_flavor")
        last_roast = session.get("last_roast")

        if last_flavor:
            results = recommend_coffees_by_flavor(last_flavor, recommended_names)
            if results:
                for item in results:
                    recommended_names.append(item["name"])
                session["recommended_names"] = recommended_names
                has_more = bool(recommend_coffees_by_flavor(last_flavor, recommended_names, limit=1))
                return render_template(
                    "result.html",
                    coffee=None,
                    coffees=results,
                    preferences=preferences,
                    has_more=has_more,
                    page_title=f"☕ 為你推薦的{last_flavor}咖啡"
                )
            else:
                # 同口味已推薦完，自動改用 AI 推薦
                results = recommend_top3(
                    preferences,
                    recent_feedback=recent_feedback,
                    excluded_names=recommended_names
                )
                if results:
                    for item in results:
                        if item["name"] not in recommended_names:
                            recommended_names.append(item["name"])
                    session["recommended_names"] = recommended_names
                    return render_template(
                        "result.html",
                        coffee=None,
                        coffees=results,
                        preferences=preferences,
                        has_more=False,
                        page_title="☕ AI 幫你推薦其他選擇",
                        message="同口味已推薦完，改為 AI 幫你推薦！"
                    )

        elif last_roast:
            results = recommend_coffees_by_roast(last_roast, recommended_names)
            if results:
                for item in results:
                    recommended_names.append(item["name"])
                session["recommended_names"] = recommended_names
                has_more = bool(recommend_coffees_by_roast(last_roast, recommended_names, limit=1))
                return render_template(
                    "result.html",
                    coffee=None,
                    coffees=results,
                    preferences=preferences,
                    has_more=has_more,
                    page_title=f"☕ 為你推薦的{last_roast}咖啡"
                )
            else:
                # 同烘焙度已推薦完，自動改用 AI 推薦
                results = recommend_top3(
                    preferences,
                    recent_feedback=recent_feedback,
                    excluded_names=recommended_names
                )
                if results:
                    for item in results:
                        if item["name"] not in recommended_names:
                            recommended_names.append(item["name"])
                    session["recommended_names"] = recommended_names
                    return render_template(
                        "result.html",
                        coffee=None,
                        coffees=results,
                        preferences=preferences,
                        has_more=False,
                        page_title="☕ AI 幫你推薦其他選擇",
                        message="同烘焙度已推薦完，改為 AI 幫你推薦！"
                    )

    elif choice == "6":
        results = recommend_coffee(
            coffees,
            preferences,
            recent_feedback=recent_feedback,
            excluded_names=recommended_names
        )
        if results:
            for item in results:
                if item["name"] not in recommended_names:
                    recommended_names.append(item["name"])
            session["recommended_names"] = recommended_names
            return render_template(
                "result.html",
                coffee=None,
                coffees=results,
                preferences=preferences,
                has_more=False,
                page_title="☕ AI 推薦給你的咖啡"
            )

    return render_template(
        "result.html",
        coffee=None,
        coffees=None,
        preferences=preferences,
        has_more=False,
        page_title="推薦結果",
        message="目前沒有可推薦的咖啡，請換個口味試試。"
    )


@app.route("/feedback", methods=["POST"])
def feedback():
    feedback_value = request.form.get("feedback")
    flavor = request.form.get("flavor")
    roast = request.form.get("roast")

    preferences = load_preferences()

    if "recent_feedback" not in session:
        session["recent_feedback"] = []

    recent_feedback = session["recent_feedback"]

    if feedback_value in ["喜歡", "不喜歡", "略過"]:
        if flavor:
            update_preferences(preferences, flavor, feedback_value)
        if roast:
            update_preferences(preferences, roast, feedback_value)
        save_preferences(preferences)

        recent_feedback.append({
            "flavor": flavor,
            "feedback": feedback_value
        })

        session["recent_feedback"] = recent_feedback[-10:]

    return redirect(url_for("recommend_after_feedback"))


@app.route("/recommend_after_feedback")
def recommend_after_feedback():
    preferences = load_preferences()
    recommended_names = session.get("recommended_names", [])
    recent_feedback = session.get("recent_feedback", [])

    results = recommend_top3(
        preferences,
        recent_feedback=recent_feedback,
        excluded_names=recommended_names
    )

    if results:
        session["current_coffees"] = results
        return render_template(
            "result.html",
            coffee=None,
            coffees=results,
            preferences=preferences,
            has_more=False,
            page_title="☕ AI 推薦給你的咖啡"
        )

    return redirect(url_for("home"))


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
