# Building-a-Recipe-Generator
Create a simple prompt that generates cooking recipes based on given ingredients.

# 🥘 Recipe Finder with Spoonacular API
This Python project allows users to input a list of available ingredients and fetches a suitable recipe from the Spoonacular API. 
It returns detailed recipe information including ingredients, steps, time required, and a link to the full recipe. Optionally, it also saves the recipe to a text file.

---
## 📌 Features
- Input ingredients and fetch a matching recipe.
- Shows:
  - Recipe title
  - Used and missing ingredients
  - Recipe image preview
  - Time required and servings
  - Step-by-step instructions
- Optionally save the recipe to a `.txt` file.
---

## 🛠️ Requirements
- Python 3.x
- `requests` library
- Install the dependency with:
  ```bash
   pip install requests
----

## 🔐 API Key
- This project uses the Spoonacular API.
- Create an account on Spoonacular.
- Navigate to your dashboard and get your free API key.
- Replace the placeholder key in the script:
  ```python
       API_KEY = "YOUR_API_KEY_HERE"
---
## 🚀 How to Run
- Save the script as recipe_finder.py.
- Run the script in terminal or any Python environment:
   [python recipe_finder.py]
- Enter a comma-separated list of ingredients when prompted:
  [What ingredients do you have? (Separate with commas): chicken, garlic, lemon]
- The script fetches and displays a matching recipe.
- If you choose to save the recipe:
   [Want to save this recipe to a text file? (yes/no): yes}
- A file named generated_recipe.txt will be created with the recipe details.

## Recipe Finder Python code step by step to understand how it works.
**🔍 Overview**
- The program:
  - Takes user-input ingredients.
  - Calls the Spoonacular API to find a matching recipe.
  - Displays the recipe title, image, ingredients, and instructions.
  - Optionally saves the recipe to a .txt file.
    
**🧱 Code Explanation**
**✅ 1. Importing Required Module:**
    ```import requests
- requests is used to make HTTP calls to the Spoonacular API.
**🔐 2. Configuration:**
    ``` API_KEY = "# ← REPLACE THIS with your key"
        BASE_URL = "https://api.spoonacular.com"    
-API_KEY: Your access key to use the Spoonacular API.
- BASE_URL: The base URL for all API endpoints.
**🧾 3. Take Input from User:**
    ```user_input = input("What ingredients do you have? (Separate with commas): ")
-Asks the user to type in a comma-separated list of ingredients, e.g., "chicken, garlic, lemon".
**🍽️ 4. Find Recipe Based on Ingredients:**
    ```find_recipe_url = f"{BASE_URL}/recipes/findByIngredients"
lookup_params = {
    "ingredients": user_input,
    "number": 1,
    "ranking": 1,
    "ignorePantry": True,
    "apiKey": API_KEY
}
- URL for the API call to search for recipes.
- number=1: Only fetches one recipe.
- ranking=1: Prioritizes recipes that use the most ingredients you have.
- ignorePantry=True: Ignores common pantry items like water, salt, etc.
  ```search_result = requests.get(find_recipe_url, params=lookup_params)
- Makes the actual API call.
**🚨 5. Handle Errors:**
  ```if search_result.status_code != 200:
    print("Hmm, something went wrong:", search_result.json())
    exit(1)
- If the API call fails, prints the error and exits the program.
**🥇 6. Parse the First Recipe:**
  ```recipe_data = search_result.json()
if not recipe_data:
    print("Couldn't find any recipe with those ingredients.")
    exit()
- If the list is empty, no recipe was found.
  ```first_recipe = recipe_data[0]
print("\n=== Found a Recipe! ===")
print(f"Title: {first_recipe['title']}")
print(f"Used: {[item['name'] for item in first_recipe['usedIngredients']]}")
print(f"Missing: {[item['name'] for item in first_recipe['missedIngredients']]}")
print(f"Image Preview: {first_recipe['image']}")
-Shows basic recipe details including:
    - Used & missing ingredients
    - Image preview link
**📋 7. Fetch Full Recipe Information:**
     ```recipe_id = first_recipe['id']
details_url = f"{BASE_URL}/recipes/{recipe_id}/information"
details_params = {
    "includeNutrition": False,
    "apiKey": API_KEY
}
details_response = requests.get(details_url, params=details_params)
- Uses the recipe ID to fetch full instructions, time, ingredients, servings, etc.
      ```if details_response.status_code != 200:
    print("Ugh, failed to fetch full recipe info:", details_response.json())
    exit()
- Handles error if second API call fails.
**📤 8. Display Full Recipe:**
   ```details = details_response.json()
print("\n=== Full Recipe Info ===")
print(f"Title: {details['title']}")
print(f"Time Required: {details['readyInMinutes']} mins")
print(f"Servings: {details['servings']}")
print(f"Link: {details['sourceUrl']}")

- Displays title, time, servings, and a link to the full recipe.
      ```print("\nIngredients Needed:")
for ing in details['extendedIngredients']:
    print(f"- {ing['original']}")
- Shows a nicely formatted ingredients list.
    ```print("\nHow to Make It:")
if details.get('instructions'):
    print(details['instructions'])
else:
    print("No instructions were provided. Might be a good time to improvise!")
- Displays instructions if available.
**💾 9. Optionally Save to File:**
  ```save_choice = input("\nWant to save this recipe to a text file? (yes/no): ").strip().lower()

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
-If user says "yes", it writes the recipe details into a file named generated_recipe.txt.
- Proper error handling in case file write fails.
  
**✅ Conclusion**
  This is a clean, well-structured script for building a basic AI-powered recipe generator based on user input ingredients using a real-world API.
  Let me know if you want enhancements like:
  Showing multiple recipe options
  Using a GUI (Tkinter)
  Sending recipe via email
  CLI tool version with flags (e.g., --save, --limit)


## 📂 Output Sample
=== Found a Recipe! ===
Title: Grilled Lemon Garlic Chicken
Used: ['chicken', 'garlic', 'lemon']
Missing: ['olive oil', 'rosemary']
Image Preview: https://spoonacular.com/recipeImages/123456-312x231.jpg

=== Full Recipe Info ===
Title: Grilled Lemon Garlic Chicken
Time Required: 30 mins
Servings: 4
Link: https://spoonacular.com/recipes/123456

Ingredients Needed:
- 2 boneless chicken breasts
- 3 cloves garlic, minced
- 1 lemon, juiced
- 2 tbsp olive oil
- 1 tsp rosemary

How to Make It:
1. Mix garlic, lemon juice, olive oil, and rosemary.
2. Marinate chicken for 15 mins.
3. Grill for 8-10 mins on each side.


## 🧠 Notes
Only one recipe is fetched ("number": 1) for simplicity. You can increase this number in the lookup_params.
ignorePantry=True will exclude common pantry items like salt, water, etc.
The script checks for possible API failures and informs the user.

