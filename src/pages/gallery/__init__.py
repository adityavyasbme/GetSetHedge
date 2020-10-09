import pandas as pd
try:
    table = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    df.to_csv('data/index_csv/SP500.csv')
except:
    print("Error in downloading SP500 index")
