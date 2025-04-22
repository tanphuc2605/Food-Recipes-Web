from flask import Blueprint, jsonify, request
from source.utils.data_loader import load_data

bp = Blueprint('recipes', __name__)

# Load data
recipes, ingredient_pairs, clustered_recipes, season_recipes = load_data()

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
        recipe for recipe in recipes
        if all(ing in recipe['ingredients'] for ing in input_ingredients)
    ]
    
    if matching_recipes:
        selected_recipe = matching_recipes[0]
        cluster = selected_recipe['cluster']
        alternatives = [
            r for r in recipes
            if r['cluster'] == cluster and r['id'] != selected_recipe['id']
        ][:3]
        return jsonify({
            'selected': selected_recipe,
            'alternatives': alternatives
        })
    
    # No exact match, return partial matches
    partial_matches = [
        {
            **recipe,
            'match_count': sum(1 for ing in input_ingredients if ing in recipe['ingredients'])
        }
        for recipe in recipes
    ]
    partial_matches = [
        r for r in partial_matches if r['match_count'] > 0
    ]
    partial_matches.sort(key=lambda x: x['match_count'], reverse=True)
    return jsonify({
        'selected': None,
        'alternatives': [
            {k: v for k, v in r.items() if k != 'match_count'}
            for r in partial_matches[:3]
        ]
    })

@bp.route('/ingredient-pairs', methods=['GET'])
def get_ingredient_pairs():
    return jsonify(ingredient_pairs[:10])