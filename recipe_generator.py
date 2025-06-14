import requests

# -- Config & Constants (probably move to a config file later) --
API_KEY = "....................................."  # ← REPLACE THIS with your key
BASE_URL = "https://api.spoonacular.com"

# -- Get input from user --
user_input = input("What ingredients do you have? (Separate with commas): ")

# -- Step 1: Try to find a matching recipe --
find_recipe_url = f"{BASE_URL}/recipes/findByIngredients"
lookup_params = {
    "ingredients": user_input,
    "number": 1,  # just grabbing one for now
    "ranking": 1,
    "ignorePantry": True,
    "apiKey": API_KEY
}

print("\nLooking up recipes... hang tight.")

search_result = requests.get(find_recipe_url, params=lookup_params)

if search_result.status_code != 200:
    print("Hmm, something went wrong:", search_result.json())
    exit(1)  # using a different code just in case

recipe_data = search_result.json()

if not recipe_data:
    print("Couldn't find any recipe with those ingredients.")
    exit()

# -- Pull out the first recipe (since we limited it to 1) --
first_recipe = recipe_data[0]
print("\n=== Found a Recipe! ===")
print(f"Title: {first_recipe['title']}")
print(f"Used: {[item['name'] for item in first_recipe['usedIngredients']]}")
print(f"Missing: {[item['name'] for item in first_recipe['missedIngredients']]}")
print(f"Image Preview: {first_recipe['image']}")

# -- Step 2: Grab the full recipe details --
recipe_id = first_recipe['id']
details_url = f"{BASE_URL}/recipes/{recipe_id}/information"

details_params = {
    "includeNutrition": False,
    "apiKey": API_KEY
}

details_response = requests.get(details_url, params=details_params)

if details_response.status_code != 200:
    print("Ugh, failed to fetch full recipe info:", details_response.json())
    exit()

details = details_response.json()

# -- Display full instructions & ingredient list --
print("\n=== Full Recipe Info ===")
print(f"Title: {details['title']}")
print(f"Time Required: {details['readyInMinutes']} mins")
print(f"Servings: {details['servings']}")
print(f"Link: {details['sourceUrl']}")

print("\nIngredients Needed:")
for ing in details['extendedIngredients']:
    print(f"- {ing['original']}")

print("\nHow to Make It:")
if details.get('instructions'):
    print(details['instructions'])
else:
    print("No instructions were provided. Might be a good time to improvise!")

# -- Optionally save to a file --
save_choice = input("\nWant to save this recipe to a text file? (yes/no): ").strip().lower()

if save_choice == "yes":
    try:
        with open("generated_recipe.txt", "w", encoding="utf-8") as f:
            f.write(f"Title: {details['title']}\n")
            f.write(f"Time Required: {details['readyInMinutes']} mins\n")
            f.write(f"Servings: {details['servings']}\n")
            f.write(f"Link: {details['sourceUrl']}\n\n")
            f.write("Ingredients:\n")
            for ing in details['extendedIngredients']:
                f.write(f"- {ing['original']}\n")
            f.write("\nInstructions:\n")
            f.write(details['instructions'] or "No instructions were provided.")
        print("✅ All done! Saved to 'generated_recipe.txt'")
    except Exception as e:
        print(f"Something went wrong while saving the file: {e}")
