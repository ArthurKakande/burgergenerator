import streamlit as st
import pandas as pd
import intellikit as ik
import time

# Define the main case base
case_base = [
    {
        'name': 'Cheeseburger',
        'ingredients': ['bun', 'beef patty', 'cheese', 'lettuce', 'tomato'],
        'steps': [
            'Place bottom bun',
            'Add beef patty',
            'Add cheese',
            'Add lettuce',
            'Add tomato',
            'Place top bun'
        ]
    },
    {
        'name': 'Chicken Burger',
        'ingredients': ['bun', 'chicken patty', 'lettuce', 'mayo'],
        'steps': [
            'Place bottom bun',
            'Add chicken patty',
            'Add lettuce',
            'Add mayo',
            'Place top bun'
        ]
    },
    {
        'name': 'Veggie Burger',
        'ingredients': ['bun', 'veggie patty', 'lettuce', 'tomato', 'onion'],
        'steps': [
            'Place bottom bun',
            'Add veggie patty',
            'Add lettuce',
            'Add tomato',
            'Add onion',
            'Place top bun'
        ]
    },
    {
        'name': 'Turkey Sandwich',
        'ingredients': ['bread', 'turkey', 'lettuce', 'tomato', 'mayo'],
        'steps': [
            'Place one slice of bread',
            'Add turkey',
            'Add lettuce',
            'Add tomato',
            'Add mayo',
            'Place another slice of bread'
        ]
    },
    {
        'name': 'Ham Sandwich',
        'ingredients': ['bread', 'ham', 'cheese', 'lettuce', 'mustard'],
        'steps': [
            'Place one slice of bread',
            'Add ham',
            'Add cheese',
            'Add lettuce',
            'Add mustard',
            'Place another slice of bread'
        ]
    },
    {
        'name': 'Chicken Wrap',
        'ingredients': ['tortilla', 'chicken', 'lettuce', 'tomato', 'ranch'],
        'steps': [
            'Place tortilla',
            'Add chicken',
            'Add lettuce',
            'Add tomato',
            'Add ranch',
            'Wrap the tortilla'
        ]
    },
    {
        'name': 'Veggie Wrap',
        'ingredients': ['tortilla', 'lettuce', 'tomato', 'cucumber', 'hummus'],
        'steps': [
            'Place tortilla',
            'Add lettuce',
            'Add tomato',
            'Add cucumber',
            'Add hummus',
            'Wrap the tortilla'
        ]
    }
]

# Define the adaptation case base
adaptation_case_base = [
    {'missing': 'beef patty', 'replacement': 'chicken patty'},
    {'missing': 'chicken patty', 'replacement': 'veggie patty'},
    {'missing': 'cheese', 'replacement': 'mayo'},
    {'missing': 'mayo', 'replacement': 'ranch'},
    {'missing': 'bread', 'replacement': 'lettuce'},
    {'missing': 'turkey', 'replacement': 'ham'},
    {'missing': 'ham', 'replacement': 'turkey'},
    {'missing': 'mustard', 'replacement': 'ranch'},
    {'missing': 'ranch', 'replacement': 'hummus'},
    {'missing': 'hummus', 'replacement': 'ranch'},
    {'missing': 'cucumber', 'replacement': 'tomato'},
    {'missing': 'tomato', 'replacement': 'cucumber'},
    {'missing': 'tortilla', 'replacement': 'lettuce'},
    {'missing': 'lettuce', 'replacement': 'cabbage'}
]

# Define available ingredients
available_ingredients = ['bun', 'chicken patty', 'lettuce', 'onion', 'bread', 'turkey', 'tomato', 'ham', 'cheese', 'mustard', 'tortilla', 'chicken', 'ranch', 'cucumber', 'hummus']

# Define a simple text-based visualization
def visualize_step(step, burger_layers, placeholder):
    if "Place bottom bun" in step:
        burger_layers.append("🥯 Bottom Bun")
    elif "Place one slice of bread" in step:
        burger_layers.append("🍞 Bread Slice")
    elif "Place tortilla" in step:
        burger_layers.append("🌯 Tortilla")
    elif "Add" in step:
        ingredient = step.split("Add ")[1]
        burger_layers.append(f"🥗 {ingredient.capitalize()}")
    elif "Place top bun" in step:
        burger_layers.append("🥯 Top Bun")
    elif "Place another slice of bread" in step:
        burger_layers.append("🍞 Bread Slice")
    elif "Wrap the tortilla" in step:
        burger_layers.append("🌯 Wrapped Tortilla")
    else:
        st.write(f"Unknown step: {step}")
    
    # Display the burger stack
    placeholder.empty()
    placeholder.write("\nCurrent Burger Stack:")
    for layer in reversed(burger_layers):
        placeholder.write(layer)
    time.sleep(1)  # Pause for visualization

# Simulate the burger assembly
def simulate_burger_assembly(steps):
    burger_layers = []
    placeholder = st.empty()
    st.write("\n🍔 Starting Burger Assembly Simulation 🍔")
    for step in steps:
        st.write(f"Step: {step}")
        visualize_step(step, burger_layers, placeholder)
    st.write("\n🍔 Burger Assembly Complete! 🍔")

# Define a CBR problem
def assemble_burger(ingredients, desired_outcome):
    df = pd.DataFrame(case_base)
    query = pd.DataFrame({
        'ingredients': [ingredients],
        'name': [desired_outcome]
    })

    # Define similarity functions
    hamming = ik.sim_hamming
    levenshtein = ik.sim_levenshtein

    similarity_functions = {
        'name': levenshtein,
        'ingredients': hamming
    }

    feature_weights = {
        'name': 0.6,
        'ingredients': 0.4
    }

    top_n = 1
    top_similar_cases = ik.linearRetriever(df, query, similarity_functions, feature_weights, top_n)

    if not top_similar_cases.empty:
        similar_case = top_similar_cases.iloc[0]
        steps = similar_case['steps']

        # Check for missing ingredients
        adapted_steps = steps.copy()
        for ingredient in ingredients:
            if ingredient not in available_ingredients:
                adaptation_df = pd.DataFrame(adaptation_case_base)
                replacement_row = adaptation_df[adaptation_df['missing'] == ingredient]
                if not replacement_row.empty:
                    replacement = replacement_row.iloc[0]['replacement']
                    adapted_steps = [step.replace(f'Add {ingredient}', f'Add {replacement}') for step in adapted_steps]

        return adapted_steps
    else:
        steps = []
        if 'bun' in ingredients:
            steps.append('Place bottom bun')
        elif 'bread' in ingredients:
            steps.append('Place one slice of bread')
        elif 'tortilla' in ingredients:
            steps.append('Place tortilla')

        for ingredient in ingredients:
            if ingredient in available_ingredients:
                steps.append(f'Add {ingredient}')
            else:
                adaptation_df = pd.DataFrame(adaptation_case_base)
                replacement_row = adaptation_df[adaptation_df['missing'] == ingredient]
                if not replacement_row.empty:
                    replacement = replacement_row.iloc[0]['replacement']
                    steps.append(f'Add {replacement}')

        if 'bun' in ingredients:
            steps.append('Place top bun')
        elif 'bread' in ingredients:
            steps.append('Place another slice of bread')
        elif 'tortilla' in ingredients:
            steps.append('Wrap the tortilla')

        new_case = {
            'name': desired_outcome,
            'ingredients': ingredients,
            'steps': steps
        }
        case_base.append(new_case)
        return steps

# Streamlit interface
st.title("Burger Generator")
st.write("This app simulates the assembly of various burgers, sandwiches, and wraps based on user-provided ingredients and desired outcomes. The app uses concepts from Case-Based Reasoning (CBR) for planning tasks and Robotic Process Automation (RPA) to assemble the snack. Where the requested ingredient isnt available, the robot will suggest a suitable replacement using adaptation knowledge obtained from what previous customers took.")
ingredients_input = st.text_input("Enter ingredients (comma-separated):")
outcome_input = st.selectbox("Select desired burger name:", ["Cheeseburger", "Chicken Burger", "Veggie Burger", "Turkey Sandwich", "Ham Sandwich", "Chicken Wrap", "Veggie Wrap"])

if st.button("Assemble Snack"):
    ingredients = [ingredient.strip() for ingredient in ingredients_input.split(',')]
    outcome = outcome_input.strip()
    steps = assemble_burger(ingredients, outcome)
    st.write("Assembling the Snack:")
    simulate_burger_assembly(steps)