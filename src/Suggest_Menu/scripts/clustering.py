import json
import numpy as np
from sklearn.cluster import KMeans

# Load cleaned recipes
with open('data/processed/tagged_recipes.json', 'r') as file:
    recipes = json.load(file)

# Get all unique ingredients
all_ingredients = list(set(ing for recipe in recipes for ing in recipe['ingredients']))

# Tạo từ điển ánh xạ nguyên liệu → chỉ số cột
ingredient_index = {ing: idx for idx, ing in enumerate(all_ingredients)}

# Create binary feature matrix
X = np.zeros((len(recipes), len(all_ingredients)))
for i, recipe in enumerate(recipes):
    for ing in recipe['ingredients']:
        if ing in ingredient_index:
            X[i, ingredient_index[ing]] = 1


# Apply K-means clustering
n_clusters = 10
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
labels = kmeans.fit_predict(X)

# Add cluster labels to recipes
for i, recipe in enumerate(recipes):
    recipe['cluster'] = int(labels[i])

# Save clustered recipes
with open('data/processed/clustered_recipes.json', 'w') as file:
    json.dump(recipes, file, indent=2)