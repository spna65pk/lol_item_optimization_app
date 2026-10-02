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
1. **Data Sourcing:** The application uses the prepared JSON files in the `data` directory. These files were created with the data collection and processing scripts in `get_data`.
2. **Heuristic Search:** It employs the **Simulated Annealing** algorithm to navigate the search space of item combinations, converging on a high-value solution based on a custom-weighted objective function.
3. **Visualization:** Real-time feedback on the algorithm's performance is provided through embedded Matplotlib plots.

### Data preparation
The `get_data` directory contains the scripts and intermediate materials used to create the JSON files consumed by the application. The preparation process includes:

- downloading champion and item data from external sources;
- filtering and transforming the downloaded data into the formats used by the optimizer;
- adding champion damage-type and other attributes required by the objective function; and
- scraping recommended items for champions and saving those recommendations.

The resulting files are stored in `data`:

- `filtered_champions.json` contains the champion data used by the optimizer;
- `filtered_items.json` contains the available item statistics, effects, prices, and icons; and
- `champs_suggested_items.json` contains champion item recommendations.

The data-preparation scripts are not required when running the application with the JSON files already present. Some scripts use external websites, Selenium, or local paths and may need configuration before they can be run again.

#### Selenium scraper setup
To run `get_data/suggested_items_dynamic_scraping_rest.py`, install Google Chrome and a matching ChromeDriver, then update the ChromeDriver path in that file. Replace the placeholder in:

```python
service = Service("********\\chromedriver-win64\\chromedriver.exe")
```

with the path to the `chromedriver.exe` file on your computer. For example:

```python
service = Service(r"C:\\tools\\chromedriver-win64\\chromedriver.exe")
```

The `r` prefix keeps Windows backslashes from being interpreted as escape sequences. The scraper uses Selenium to visit the champion build pages and produces `champs_suggested_items.json`.

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
├── data/                         # JSON files consumed by the application
│   ├── champs_suggested_items.json
│   ├── filtered_champions.json
│   └── filtered_items.json
├── get_data/                     # Scripts and materials used to prepare data/
│   ├── Add_to_filtered_champs_data_dmg_type.py
│   ├── CreateDmgTypeFileFromTXT.py
│   ├── items_in_one.py
│   ├── one_json_file.py
│   ├── przedmioty_lista.py
│   ├── suggested_items_dynamic_scraping_rest.py
│   ├── dodac parametry.txt
│   └── tests_.ipynb
├── src/                          # Application source code
│   ├── gui_app.py
│   └── optimizer_logic.py
├── .gitignore
├── README.md
└── requirements.txt
```

---
