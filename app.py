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


def recommend_top3(preferences, excluded_names=None):
    if excluded_names is None:
        excluded_names = []

    sorted_flavors = sorted(preferences.items(), key=lambda x: x[1], reverse=True)

    results = []

    for flavor, score in sorted_flavors:
        for coffee in coffees:
            if coffee["flavor"] == flavor and coffee["name"] not in excluded_names:
                results.append(coffee)

                if len(results) == 3:
                    return results

    return results


def update_preferences(preferences, flavor, feedback):
    if feedback == "喜歡":
        preferences[flavor] += 1
    elif feedback == "不喜歡":
        preferences[flavor] -= 1