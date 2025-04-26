import pandas as pd
import numpy as np

df = pd.read_csv("Model_Training/Food_Calories_Data/food_nutrition_data.csv")
df = df.set_index(df["Food_Item"])

def get_items(item):
    if item in df["Food_Item"]:
        return df.loc[item].to_json()

get_items("Apple_Pie")
