import os
import json

def load_data():
    # Thư mục hiện tại là /source/utils → đi lên 2 cấp để tới thư mục gốc
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..', '..'))
    data_path = os.path.join(project_root, 'data', 'processed', 'cleaned_recipes.json')
    pairs_path = os.path.join(project_root, 'data', 'processed', 'ingredient_pairs.json')
    clustered_path = os.path.join(project_root, 'data', 'processed', 'clustered_recipes.json')
    season_path = os.path.join(project_root, 'data', 'processed', 'season_recipes.json')
    ingredient_subs_path = os.path.join(project_root, 'data', 'processed', 'ingredient_subs.json')
    with open(data_path, 'r', encoding='utf-8') as file:
        recipes = json.load(file)

    with open(pairs_path, 'r', encoding='utf-8') as file:
        ingredient_pairs = json.load(file)
    
    with open(clustered_path, 'r', encoding='utf-8') as file:
        clustered_recipes = json.load(file)
        
    with open(season_path, 'r', encoding='utf-8') as file:
        season_recipes = json.load(file)     
        
    with open(ingredient_subs_path, 'r', encoding='utf-8') as file:
        ingredient_subs = json.load(file) 
          
    return recipes, ingredient_pairs, clustered_recipes,season_recipes,ingredient_subs
