from flask import Blueprint, jsonify, request
from source.utils.data_loader import load_data

bp = Blueprint('recipes', __name__)

# Load data
recipes, ingredient_pairs, clustered_recipes, season_recipes,ingredient_subs = load_data()

@bp.route('/recipes', methods=['GET'])
def get_recipes():
    ingredients = request.args.get('ingredients', '')
    if ingredients:
        input_ingredients = [ing.strip().lower() for ing in ingredients.split(',')]
        filtered_recipes = [
            recipe for recipe in recipes
            if all(ing in recipe['ingredients'] for ing in input_ingredients)
        ]
        return jsonify(filtered_recipes)
    return jsonify(recipes)

@bp.route('/season-recipes', methods=['GET'])
def get_season_recipes():
    ingredients = request.args.get('ingredients', '')
    if ingredients:
        input_ingredients = [ing.strip().lower() for ing in ingredients.split(',')]
        filtered_recipes = [
            recipe for recipe in recipes
            if all(ing in recipe['ingredients'] for ing in input_ingredients)
        ]
        return jsonify(filtered_recipes)
    return jsonify(season_recipes)

@bp.route('/recipes/search', methods=['POST'])
def search_recipes():
    data = request.get_json()
    if not data or 'ingredients' not in data:
        return jsonify({'error': 'Ingredients required'}), 400

    input_ingredients = [ing.strip().lower() for ing in data['ingredients']]
    
    # Find exact matches
    matching_recipes = [
        recipe for recipe in season_recipes
        if all(ing in recipe['ingredients'] for ing in input_ingredients)
    ]
    
    if matching_recipes:
        selected_recipe = matching_recipes[0]
        alternatives = [
            r for r in season_recipes
            if r['id'] != selected_recipe['id']
        ]
        return jsonify({
            'matching': matching_recipes,
        })
# No exact match, find partial matches with replacements
    partial_matches = []
    for recipe in season_recipes:
        matched = set(input_ingredients) & set(recipe["ingredients"])
        missing = set(recipe["ingredients"]) - set(input_ingredients)

        # Tìm nguyên liệu thay thế
        replacements = {}
        if ingredient_subs:
            for miss in missing:
                if miss in ingredient_subs:
                    for sub in ingredient_subs[miss]:
                        if sub in input_ingredients:
                            replacements[miss] = sub
                            break
                        
        partial_matches.append({
            **recipe,
            'match_count': len(matched),
            'missing_count': len(missing),
            'possible_replacements': replacements
        })

    partial_matches = [r for r in partial_matches if r['match_count'] > 0]
    partial_matches.sort(key=lambda x:(-x["match_count"], x["missing_count"]))

    return jsonify({
        'matching': None,
        'alternatives': [
            {
                k: v for k, v in r.items() if k != 'match_count' and k != 'missing_count'
            } for r in partial_matches[:3]
        ]
    })

@bp.route('/ingredient-pairs', methods=['GET'])
def get_ingredient_pairs():
    return jsonify(ingredient_pairs[:10])