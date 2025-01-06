
# Burger Assembler App

## Description

The Burger Generator is an interactive Streamlit application that simulates the assembly of various burgers, sandwiches, and wraps based on user-provided ingredients and desired outcomes. This app leverages concepts such as Case-Based Reasoning (CBR) for planning, adaptation, and robotic process automation to provide a dynamic and engaging user experience.

## Key Concepts

- **Case-Based Reasoning (CBR):** The app uses a case base of predefined recipes to find the most similar existing recipe based on the user's input. It retrieves the closest match using similarity functions and feature weights.
  
- **Adaptation:** If the exact ingredients are not available, the app adapts the recipe by replacing missing ingredients with suitable alternatives from an adaptation case base. (Available ingredients: bun, chicken patty, lettuce, onion, bread, turkey, tomato, ham, cheese, mustard, tortilla, chicken, ranch, cucumber, hummus)

- **Robotic Process Automation (RPA):** The app simulates the step-by-step assembly of the selected recipe in real-time, providing a visual representation of the process.

## Features

- **Interactive User Interface:** Users can input ingredients and select the desired outcome using a dropdown menu.
- **Real-Time Simulation:** The app visually simulates the assembly process, displaying each step with a brief pause for better user engagement.
- **Dynamic Adaptation:** The app adapts recipes based on available ingredients, ensuring a feasible assembly process even with missing components.

This app demonstrates the practical application of CBR and adaptation in a fun and educational context, making it an excellent tool for learning and experimentation.

## Implementation
This project is a Streamlit application that allows users to input ingredients and desired outcomes to assemble burgers. The app utilizes a case-based reasoning approach to suggest assembly steps based on user input.

## Project Structure

- `app.py`: Contains the main logic for the Streamlit app, including the case base and the function to process user input.
- `requirements.txt`: Lists the dependencies required for the project.

## Requirements

To run this application, you need to have Python installed along with the following libraries:

- Streamlit
- pandas
- intellikit

## Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required libraries using pip:

```
pip install -r requirements.txt
```

## Running the App

To run the Streamlit app, execute the following command in your terminal:

```
streamlit run app.py
```

This will start the Streamlit server and open the app in your default web browser.

## Usage

1. Enter the ingredients you have available.
2. Specify the desired burger outcome.
3. The app will display the steps to assemble the burger based on the input provided.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the app.
