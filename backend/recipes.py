import requests
from collections import Counter

MAX_INGREDIENTS = 20

def search_by_ingredient(ingredient):
    res = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}")
    data = res.json()
    if data["meals"]:
        return [meal["idMeal"] for meal in data["meals"]]

    return []

def get_best_meal_id(labels):
    meal_counts = Counter()

    for label in labels:
        meal_ids = search_by_ingredient(label)
        meal_counts.update(meal_ids)
    
    if not meal_counts:
        return None
    
    return max(meal_counts, key=meal_counts.get)

def get_full_recipe(meal_id):
    res = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}")
    full_meal = res.json()["meals"][0]

    ingredients = []
    for i in range(1, MAX_INGREDIENTS + 1):
        ingredient = full_meal.get(f"strIngredient{i}", "")
        measure = full_meal.get(f"strMeasure{i}", "")
        if ingredient and ingredient.strip():
            ingredients.append(f"{measure.strip()} {ingredient.strip()}")

    return {
        "name": full_meal["strMeal"],
        "category": full_meal["strCategory"],
        "instructions": full_meal["strInstructions"],
        "ingredients": ingredients,
        "thumbnail": full_meal["strMealThumb"]
    }

def find_best_recipe(labels):
    best_id = get_best_meal_id(labels)

    if best_id is None:
        return {
            "name": "No match found",
            "ingredients": [],
            "instructions": "Try different ingredients"
        }
    
    return get_full_recipe(best_id)