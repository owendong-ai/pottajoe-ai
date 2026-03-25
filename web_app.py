from flask import Flask, render_template, request, redirect, url_for, session
from app import recommend_coffee_by_flavor, recommend_top3, update_preferences
from user_data import load_preferences, save_preferences

app = Flask(__name__)
app.secret_key = "pottajoe_secret_key"


@app.route("/")
def home():
    preferences = load_preferences()
    return render_template("index.html", preferences=preferences)


@app.route("/recommend", methods=["POST"])
def recommend():
    choice = request.form.get("choice")
    preferences = load_preferences()

    if "recommended_names" not in session:
        session["recommended_names"] = []

    recommended_names = session["recommended_names"]

    flavor_map = {
        "1": "濃郁",
        "2": "果香",
        "3": "堅果",
        "4": "花香"
    }

    # 先處理一般單一推薦
    if choice in flavor_map:
        flavor = flavor_map[choice]
        session["last_flavor"] = flavor
        session["recommended_names"] = []

        coffee = recommend_coffee_by_flavor(flavor, [])
        if coffee:
            session["current_coffee"] = coffee
            session["current_coffees"] = []
            session["recommended_names"] = [coffee["name"]]
            return render_template(
                "result.html",
                coffee=coffee,
                coffees=None,
                preferences=preferences
            )

    # 再推薦一個
    elif choice == "5":
        last_flavor = session.get("last_flavor")
        if last_flavor:
            coffee = recommend_coffee_by_flavor(last_flavor, recommended_names)
            if coffee:
                recommended_names.append(coffee["name"])
                session["recommended_names"] = recommended_names
                session["current_coffee"] = coffee
                session["current_coffees"] = []
                return render_template(
                    "result.html",
                    coffee=coffee,
                    coffees=None,
                    preferences=preferences
                )

    # AI 幫我推薦：一次推薦 Top 3
    elif choice == "6":
        coffees = recommend_top3(preferences, recommended_names)
        if coffees:
            session["current_coffees"] = coffees
            session["current_coffee"] = None

            for item in coffees:
                if item["name"] not in recommended_names:
                    recommended_names.append(item["name"])

            session["recommended_names"] = recommended_names

            return render_template(
                "result.html",
                coffee=None,
                coffees=coffees,
                preferences=preferences
            )

    return render_template(
        "result.html",
        coffee=None,
        coffees=None,
        preferences=preferences,
        message="目前沒有可推薦的咖啡，請換個口味試試。"
    )


@app.route("/feedback", methods=["POST"])
def feedback():
    feedback_value = request.form.get("feedback")
    flavor = request.form.get("flavor")

    preferences = load_preferences()

    if flavor and feedback_value in ["喜歡", "不喜歡", "略過"]:
        update_preferences(preferences, flavor, feedback_value)
        save_preferences(preferences)

    return redirect(url_for("recommend_after_feedback"))


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))

@app.route("/recommend_after_feedback")
def recommend_after_feedback():
    preferences = load_preferences()
    recommended_names = session.get("recommended_names", [])

    coffees = recommend_top3(preferences, recommended_names)

    if coffees:
        session["current_coffees"] = coffees
        return render_template(
            "result.html",
            coffee=None,
            coffees=coffees,
            preferences=preferences
        )

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)