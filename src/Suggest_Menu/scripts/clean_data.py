import json
from collections import Counter
import inflect


p = inflect.engine()
# Load the JSON data
with open('data/raw/test.json', 'r') as file:
    recipes = json.load(file)

# Common words to remove for standardization
remove_words = [
    'fresh', 'ground', 'chopped', 'dried', 'sliced', 'minced', 'grated',
    'finely', 'coarse', 'large', 'small', 'reduced', 'fat', 'free', 'low',
    'sodium', 'unsalted', 'cooked', 'roasted', 'toasted', 'raw', 'lean',
    'extra', 'virgin', 'light', 'whole', 'boneless', 'skinless', 'halves'
]

def clean_ingredient(ingredient):
    words = ingredient.lower().split()
    cleaned = [word for word in words if word not in remove_words and word]
    cleaned_name = ' '.join(cleaned)

    try:
        singular = p.singular_noun(str(cleaned_name))  # đảm bảo truyền vào là str
        cleaned_name = singular if singular else cleaned_name
    except Exception:
        pass  # nếu có lỗi, cứ giữ nguyên tên

    ingredient_map = {
        'all-purpose flour': 'flour',
        'white sugar': 'sugar',
        'corn starch': 'cornstarch',
        'soy sauce': 'soy sauce',
        'black pepper': 'pepper',
        'white onion': 'onion',
        'yellow onion': 'onion',
        'purple onion': 'onion',
        'green onion': 'scallion',
        'spring onion': 'scallion',
        'green bell pepper': 'bell pepper',
        'red bell pepper': 'bell pepper',
        'chicken broth': 'chicken stock',
        'garlic clove': 'garlic',
        'jalapeno chili': 'jalapeno',
        'cilantro fresh': 'cilantro',
        'parmesan cheese': 'parmesan',
        'mozzarella cheese': 'mozzarella',
        'cheddar cheese': 'cheddar',
        'olive oil': 'oliveoil',
        'vegetable oil': 'vegetableoil'
    }

    return ingredient_map.get(cleaned_name, cleaned_name)


def generate_dish_name(ingredients):
    all_ingredients = [ing for recipe in recipes for ing in recipe['ingredients']]
    ingredient_freq = Counter(all_ingredients)
    sorted_ings = sorted(ingredients, key=lambda x: ingredient_freq[x])
    top_ings = sorted_ings[:2]
    return f"{top_ings[0].capitalize()} {'and' if len(top_ings) > 1 else ''} {top_ings[1].capitalize() if len(top_ings) > 1 else ''} Dish".strip()

# Clean the data
cleaned_recipes = []
for recipe in recipes:
    cleaned_ingredients = list(set(clean_ingredient(ing) for ing in recipe['ingredients'] if clean_ingredient(ing)))
    dish_name = generate_dish_name(cleaned_ingredients)
    cleaned_recipes.append({
        'id': recipe['id'],
        'name': dish_name,
        'ingredients': cleaned_ingredients,
        'cuisine': 'Generic'
    })

# Save cleaned data
with open('data/processed/cleaned_recipes.json', 'w') as file:
    json.dump(cleaned_recipes, file, indent=2)

# Generate ingredient co-occurrence
ingredient_pairs = Counter()
for recipe in cleaned_recipes:
    ingredients = sorted(recipe['ingredients'])
    for i in range(len(ingredients)):
        for j in range(i + 1, len(ingredients)):
            pair = (ingredients[i], ingredients[j])
            ingredient_pairs[pair] += 1

# Save top 50 ingredient pairs
top_pairs = [{'pair': list(pair), 'count': count} for pair, count in ingredient_pairs.most_common(50)]
with open('data/processed/ingredient_pairs.json', 'w') as file:
    json.dump(top_pairs, file, indent=2)
    
    
def tag_season(cleaned_recipe):
    ings = set(cleaned_recipe["ingredients"])
    name = cleaned_recipe["name"].lower()

    summer_keywords = {"cucumber", "mint", "basil", "salad", "lemon", "smoothie", "juice", "watermelon", "ice cream", "grilled", "corn", "peach", "tomato", "sorbet", "popsicle", "berries"}
    winter_keywords = {"soup", "hotpot", "broth", "ginger", "stew", "chili", "carrot", "beet", "leek", "cinnamon", "roast", "potatoes", "apple pie", "hot chocolate", "rosemary", "nutmeg"}
    autumn_keywords = {"pumpkin", "apple", "sweet potato", "bake", "mushroom", "cabbage", "cranberry", "squash", "pecan", "cinnamon", "hazelnut", "caramel", "fig", "maple", "brussels sprouts"}
    spring_keywords = {"peas", "spinach", "asparagus", "light", "green", "strawberries", "mint", "cherry", "artichoke", "radish", "lemon", "herbs", "cress", "fennel", "green beans"}

    if ings & summer_keywords or any(word in name for word in ["salad", "smoothie", "juice"]):
        return "summer"
    elif ings & winter_keywords or any(word in name for word in ["soup", "hotpot", "stew"]):
        return "winter"
    elif ings & autumn_keywords:
        return "autumn"
    elif ings & spring_keywords:
        return "spring"
    return "unknown"

for cleaned_recipe in cleaned_recipes:
    cleaned_recipe["season"] = tag_season(cleaned_recipe)

# Lưu file mới có thêm trường "season"
with open("data/processed/season_recipes.json", "w") as f:
    json.dump(cleaned_recipes, f, indent=2)