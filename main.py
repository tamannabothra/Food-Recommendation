import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns

#reading of the files
food = pd.read_csv("food.csv")
ratings = pd.read_csv("ratings.csv")

#pivot table
dataset = ratings.pivot_table(index='Food_ID',columns='User_ID',values='Rating')
dataset.fillna(0,inplace=True)

#main Recommendation Function
def food_recommendation(Food_Name):
    n = 10
    FoodList = food[food['Name'].str.contains(Food_Name)]
    if len(FoodList):
        Foodi= FoodList.iloc[0]['Food_ID']
        Foodi = dataset[dataset['Food_ID'] == Foodi].index[0]
        distances , indices = model.kneighbors(csr_dataset[Foodi],n_neighbors=n+1)
        Food_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        Recommendations = []
        for val in Food_indices:
            Foodi = dataset.iloc[val[0]]['Food_ID']
            i = food[food['Food_ID'] == Foodi].index
            Recommendations.append({'Name':food.iloc[i]['Name'].values[0],'Distance':val[1]})
        df = pd.DataFrame(Recommendations,index=range(1,n+1))
        return df['Name']
    else:
        return "No Similar Foods."

#remove sparsity
csr_dataset = csr_matrix(dataset.values)
dataset.reset_index(inplace=True)

#using algorithm
model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
model.fit(csr_dataset)

food_recommendation('summer squash salad')
