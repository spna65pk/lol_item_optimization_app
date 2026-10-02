# League of Legends Item Optimizer
**A heuristic optimization tool using Simulated Annealing to find near-optimal item builds.**

## Authors
This project was developed by a two-person team with responsibilities split on:
- core optimization algorithm (Simulated Annealing) and the Graphical User Interface (GUI).
- web scraping, data preparation and designing objective function.

---

## Project Overview
Desktop application designed to solve the complex problem of selecting the best set of items for a champion in game **League of Legends**. 

The application takes into account:
- The user's champion.
- The composition of the enemy team.
- Gold constraints and item tier limitations.

### How it works:
1. **Data Sourcing:** The application uses JSON data files containing champion and item statistics, which were obtained through web scraping of community-driven data sources.
2. **Heuristic Search:** It employs the **Simulated Annealing** algorithm to navigate the search space of item combinations, converging on a high-value solution based on a custom-weighted objective function.
3. **Visualization:** Real-time feedback on the algorithm's performance is provided through embedded Matplotlib plots.

---

## Application Interface

### 1. Configuration Window
Users can parameterize the algorithm (Initial Temperature, Alpha, Gold Limit) and select the champion composition of the match.
<img width="898" height="1027" alt="Image" src="https://github.com/user-attachments/assets/af6f7151-94c6-471f-af2e-628bee7307db" />

### 2. Results & Analysis
The output window displays the best found item build along with their icons and technical plots showing the temperature decay and objective function convergence.
<img width="1294" height="1029" alt="Image" src="https://github.com/user-attachments/assets/9142ee4d-7fe8-4c1f-80d8-6637956549c4" />

---

## Installation & Usage

### Requirements
The project requires Python 3.10+ and the libraries listed in the `requirements.txt` file.

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2.  Run the application:
    Navigate to the project root directory and execute:
    ```bash
    python src/gui_app.py
    ```

---

Project Structure
```text
.
├── data
│   ├── champs_suggested_items.json
│   ├── filtered_champions.json
│   └── filtered_items.json
├── src
│   ├── gui_app.py
│   └── optimizer_logic.py
├── .gitignore
├── README.md
└── requirements.txt
```

---
