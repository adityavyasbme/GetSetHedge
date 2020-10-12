#Project Structure

```bash
.
├── Dockerfile
├── LICENSE
├── README.md
├── data
│   ├── features # CUSTOM FEATURES BACKUP
│   ├── images # IMAGES TO USE IN STREAMLIT APP
│   └── index_csv # STORE INDEX FILES HERE
├── logs #TO STORE LOGS
├── requirements.txt
├── src
│   ├── eda #EXPLORATORY DATA ANALYSIS TOOL
│   │   ├── child.py
│   │   ├── government.py
│   │   ├── graphs.py
│   │   ├── hyperparameter.py
│   │   ├── input.py
│   │   └── parent.py
│   ├── errors.py # TODO: USER DEFINED ERRORS
│   ├── features # FEATURE CONSTRUCTION
│   │   ├── features.py
│   │   └── indicators
│   │       ├── __init__.py
│   │       └── custom_indicator.py
│   ├── hedging # HEDGING PAGE FLOW
│   │   ├── caller.py
│   │   ├── division.py
│   │   ├── factors #FACTOR CONSTRUCTION
│   │   │   ├── beta.py
│   │   │   └── momentum.py
│   │   └── parser.py
│   ├── helper.py #GLOBAL FUNCTIONS SUPPORT FILE
│   ├── main.py #MAIN RUNNER OF THE APP
│   ├── pages # FRONT END
│   │   ├── about.py
│   │   ├── data.py
│   │   ├── gallery
│   │   │   ├── index.py
│   │   │   └── readme.md
│   │   ├── hedging.py
│   │   ├── home.py
│   │   └── readme.md
│   └── readme.md
├── stream.py # TODO: CREATE RUN.SH
├── tests
│   └── code_test
│       └── test_example.py #TEST FILE
```
