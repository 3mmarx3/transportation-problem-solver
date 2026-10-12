Transportation Problem Solver 🚛

A Streamlit-based interactive web application designed to solve the Transportation Problem. This tool allows users to input cost, supply, and demand data, and calculates the most cost-effective distribution of goods using various mathematical algorithms. It also provides a visual representation of the final transportation network.

✨ Features

Dynamic Data Input: Easily adjust the number of Sources and Destinations (from 2 up to 10).

Interactive Data Tables: User-friendly grid to input the Cost Matrix, Supply quantities, and Demand quantities.

Balance Check: Automatically verifies if total supply equals total demand and alerts the user if the problem is unbalanced.

Multiple Solution Algorithms:

Least Cost Method (LCM)

Vogel's Approximation Method (VAM)

Absolute Optimal Solution using Linear Programming (SciPy Highs method)

Network Visualization: Generates an interactive bipartite graph using NetworkX to visualize the optimal transportation routes and allocated quantities.

🛠️ Technology Stack

This project is built with Python and utilizes the following libraries:

Streamlit: For the interactive web interface.

NumPy & Pandas: For data manipulation and matrix operations.

SciPy: For calculating the absolute optimal solution.

NetworkX & Matplotlib: For rendering the network graph.

🚀 Installation and Setup

Follow these steps to run the project locally on your machine:

Clone the repository:

git clone https://github.com/3mmarx3/transportation-problem-solver.git
cd transportation-problem-solver

Install the required dependencies:

pip install streamlit numpy pandas scipy networkx matplotlib

Run the application:

streamlit run app.py

📖 How to Use

Set the desired number of Sources and Destinations using the numeric inputs at the top.

Fill in the Cost Matrix with the unit transportation costs.

Enter the available quantities in the Supply table and the required quantities in the Demand table.

Click the "Solve Problem" button.

Navigate through the tabs to compare the results of the Least Cost Method, Vogel's Method, the Absolute Optimal Solution, and view the Network Graph.
