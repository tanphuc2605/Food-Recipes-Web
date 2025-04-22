import json
from collections import Counter

with open('data/processed/season_recipes.json', 'r') as file:
    recipes = json.load(file)


def suggest_alternative_menu(user_ingredients, recipes, ingredient_subs=None, cluster=None, top_n=5):
    suggestions = []

    for recipe in recipes:
        if cluster is not None and recipe.get("cluster") != cluster:
            continue

        matched = set(user_ingredients) & set(recipe["ingredients"])
        missing = set(recipe["ingredients"]) - set(user_ingredients)

        replacements = {}
        if ingredient_subs:
            for miss in missing:
                if miss in ingredient_subs:
                    for sub in ingredient_subs[miss]:
                        if sub in user_ingredients:
                            replacements[miss] = sub
                            break

        suggestions.append({
            "id": recipe["id"],
            "name": recipe["name"],
            "match_count": len(matched),
            "missing_count": len(missing),
            "possible_replacements": replacements
        })

    suggestions.sort(key=lambda x: (-x["match_count"], x["missing_count"]))
    return suggestions[:top_n]

def suggest_by_season(recipes, season, seasonal_ings, top_n=5):
    season_ings = set(seasonal_ings.get(season.lower(), []))
    suggestions = []

    for recipe in recipes:
        overlap = set(recipe["ingredients"]) & season_ings
        suggestions.append({
            "id": recipe["id"],
            "name": recipe["name"],
            "season_match": len(overlap),
            "ingredients_in_season": list(overlap)
        })

    suggestions.sort(key=lambda x: -x["season_match"])
    return suggestions[:top_n]

def count_recipes_by_season(recipes):
    counter = Counter(recipe.get("season", "unknown") for recipe in recipes)
    return counter

if __name__ == "__main__":

    # Nhập nguyên liệu từ người dùng
    print("Nhập danh sách nguyên liệu bạn hiện có (cách nhau bằng dấu phẩy):")
    user_input = input(">> ")
    user_ingredients = [ing.strip().lower() for ing in user_input.split(',') if ing.strip()]

    # Nhập cluster ID (nếu muốn lọc theo nhóm)
    cluster_input = input("Bạn có muốn lọc theo cluster cụ thể không? (nhập số hoặc để trống): ")
    cluster_id = int(cluster_input) if cluster_input.strip().isdigit() else None

    # Nhập mùa nếu có
    season_input = input("Bạn muốn gợi ý theo mùa nào không? (spring/summer/autumn/winter hoặc để trống): ").strip().lower()

    # Danh sách thay thế nguyên liệu (mở rộng)
    ingredient_subs = {
        "butter": ["oil", "margarine", "ghee"],
        "white sugar": ["brown sugar", "honey", "maple syrup"],
        "milk": ["soy milk", "almond milk", "oat milk"],
        "cheddar": ["mozzarella", "parmesan", "gouda"],
        "egg": ["egg white", "egg yolk", "flaxseed meal"],
        "flour": ["whole wheat flour", "almond flour", "oat flour"],
        "salt": ["soy sauce", "miso paste"],
        "lemon juice": ["lime juice", "vinegar"],
        "cream": ["milk", "evaporated milk"],
        "yogurt": ["sour cream", "buttermilk"],
        "mayonnaise": ["greek yogurt", "avocado"],
        "onion": ["shallot", "leek"],
        "garlic": ["garlic powder", "onion powder"],
        "vinegar": ["lemon juice", "lime juice"],
        "oil": ["olive oil", "canola oil", "vegetable oil"],
        "rice": ["quinoa", "couscous", "cauliflower rice"]
    }

    seasonal_ingredients = {
        "spring": ["asparagus", "peas", "mint", "spinach", "strawberries", "radish", "artichoke", "lettuce", "green onion"],
        "summer": ["tomato", "zucchini", "corn", "cucumber", "basil", "watermelon", "bell pepper", "eggplant", "green beans", "peach", "cherry"],
        "autumn": ["pumpkin", "apple", "sweet potato", "mushroom", "cabbage", "pear", "turnip", "squash", "cauliflower"],
        "winter": ["kale", "broccoli", "carrot", "ginger", "beet", "leek", "potato", "celery", "onion", "parsnip"]
    }

    if season_input in seasonal_ingredients:
        print(f"\n\nGợi ý thực đơn theo mùa {season_input.capitalize()}:")
        season_suggestions = suggest_by_season(recipes, season_input, seasonal_ingredients)
        for s in season_suggestions:
            print(f"\nMón: {s['name']}")
            print(f"  Nguyên liệu theo mùa: {s['season_match']} nguyên liệu")
            print(f"  Danh sách: {', '.join(s['ingredients_in_season'])}")
    else:
        suggestions = suggest_alternative_menu(user_ingredients, recipes, ingredient_subs, cluster=cluster_id)

        print("\n\nGợi ý thực đơn phù hợp nhất:")
        for s in suggestions:
            print(f"\nMón: {s['name']}")
            print(f"  Nguyên liệu đã có: {s['match_count']} nguyên liệu")
            print(f"  Thiếu: {s['missing_count']} nguyên liệu")
            if s['possible_replacements']:
                print("  Gợi ý thay thế:")
                for miss, replace in s['possible_replacements'].items():
                    print(f"    {miss} -> {replace}")
            else:
                print("  (Không có gợi ý thay thế phù hợp)")

    # Thống kê số món theo mùa
    season_stats = count_recipes_by_season(recipes)
    print("\n\nThống kê số món ăn theo mùa:")
    for season, count in season_stats.items():
        print(f"  {season.capitalize()}: {count} món")
