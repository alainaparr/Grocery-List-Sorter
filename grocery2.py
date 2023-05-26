import inflect

# Instantiate an Inflector object for handling singular/plural conversions
inflector = inflect.engine()

# Define the grocery categories and the items in each category
categories = {
    "dairy": ["milk", "cheese", "yogurt", "butter", "cream"],
    "grains": ["bread", "rice", "pasta", "cereal", "flour"],
    "fruits": ["apple", "banana", "orange", "grape", "strawberry"],
    "vegetables": ["carrot", "broccoli", "lettuce", "tomato", "cucumber"],
    "meats": ["chicken", "beef", "pork", "lamb", "turkey"],
    "seafood": ["salmon", "tuna", "shrimp", "crab", "lobster"],
    "snacks": ["chips", "popcorn", "pretzels", "cookies", "candy"],
    "beverages": ["water", "soda", "juice", "coffee", "tea"],
}

# Function to categorize the items
def categorize_item(item, categories):
    # Convert the item to its singular form, if it's plural
    singular_item = inflector.singular_noun(item) or item
    
    # Check if the item belongs to any of the categories by iterating through them
    for category, items in categories.items():
        if singular_item.lower() in items:
            return category
        
    # If the item doesn't belong to any category, return "other"
    return "other"

# Function to suggest items based on partial input
def suggest_items(partial_item, categories):
    # Convert the partial item to its singular form, if it's plural
    singular_partial_item = inflector.singular_noun(partial_item) or partial_item

    # Initialize a list to store suggestions
    suggestions = []

    # Check if any item in the categories starts with the partial item
    for items in categories.values():
        for item in items:
            if item.startswith(singular_partial_item) or item.startswith(partial_item):
                # Add the item to the suggestions list if it matches the partial item
                suggestions.append(item)
    
    # Return the list of suggestions
    return suggestions

# Function to process user input and extract quantity, item, and unit
def process_input(input_str):
    # Split the input string into words
    words = input_str.split()

    # Initialize variables to store item, quantity, and unit
    item = None
    quantity = None
    unit = None

    # Iterate over the words to find quantity, item, and unit
    for idx, word in enumerate(words):
        if word.isdigit():
            # If the word is a number, set the quantity
            quantity = int(word)
        elif not item:
            # If the item has not been set, set the item
            item = word
            # If the next word is not a digit, set the unit
            if idx < len(words) - 1 and not words[idx + 1].isdigit():
                unit = words[idx + 1]
                break

    # Return the quantity, item, and unit
    return quantity, item, unit

# Input the grocery list
# Initialize an empty dictionary for the grocery list
grocery_list = {}

# Prompt the user to enter their grocery items with quantities
print("Enter your grocery items with their quantities (e.g., '3 apples'). Type 'done' when finished.")
# Loop until the user types 'done'
while True:
    user_input = input("> ").lower()
    if user_input == "done":
        break

    quantity, item, unit = process_input(user_input)

    if quantity and item:
        if not unit:
            unit = "unit(s)"

        suggestions = suggest_items(item, categories)
        if len(suggestions) == 1:
            item = suggestions[0]
        elif len(suggestions) > 1:
            print(f"Did you mean: {', '.join(suggestions)}?")
            continue
        else:
            print(f"Item '{item}' not found in the database. Adding it to 'other' category.")

        category = categorize_item(item, categories)
        if category not in grocery_list:
            grocery_list[category] = {}
        if (item, unit) in grocery_list[category]:
            grocery_list[category][(item, unit)] += quantity
        else:
            grocery_list[category][(item, unit)] = quantity
    else:
        print("Invalid input. Please try again.")

# Print the sorted grocery list
print("\nYour sorted grocery list:")
for category, items in grocery_list.items():
    print(f"\n{category.capitalize()}:")
    for (item, unit), quantity in items.items():
        print(f"  {quantity} {unit} of {item}")