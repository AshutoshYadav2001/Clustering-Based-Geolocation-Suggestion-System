import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation
import geopandas as gpd
import matplotlib.cm as cm
import folium
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Image
from IPython.core.display import HTML
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize
print("All packages imported!")

dfstudents=pd.read_csv('food_coded.csv')

dfclean=dfstudents[['cook','eating_out','employment','ethnic_food','exercise','fruit_day','income','on_off_campus','pay_meal_out','sports','veggies_day']]
dfclean.dropna(axis=0,inplace=True)
dfclean.head()

plt.figure(figsize=(20, 10))
#plt.xticks(rotation='vertical')
sns.boxplot

ax = sns.boxplot(data = dfclean)
ax.tick_params(labelsize=20)
plt.xticks(rotation=45, ha='right')
plt.show()

# set number of clusters
kclusters = 3

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(dfclean)
dfclean['Cluster']=kmeans.labels_

fig, axes = plt.subplots(1,kclusters, figsize=(20, 10), sharey=True)
axes[0].set_ylabel('Coded Values', fontsize=25)

for k in range(kclusters):
    plt.sca(axes[k])
    plt.xticks(rotation=45,ha='right')
    sns.boxplot(data = dfclean[dfclean['Cluster'] == k].drop('Cluster',1), ax=axes[k])

plt.show()

# Finding the students a home

import requests
import pandas as pd
from pandas.io.json import json_normalize

url = "https://api.foursquare.com/v3/places/nearby?ll=30.4195%2C77.9668&query=hostel%2C%20PG&limit=50&intent=browse&radius=5"
#url = "https://api.foursquare.com/v3/places/nearby?ll=30.4172%2C77.9676&query=Hostel%2C%20PG&limit=50"

headers = {
    "accept": "application/json",
    "Authorization": "fsq3bwgrZ8jL2HXYqHqSAsg5REy1ti8FL7rFKjyCKovI3TQ="
}

# Now, we pull the results of the query into a json file.
response = requests.get(url, headers=headers)
data = response.json()
places = data['results']
# transform results into a dataframe
dataframe = json_normalize(places)
dataframe
#print(dataframe)

filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['geocodes.main.latitude', 'geocodes.main.longitude','fsq_id','distance']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']

    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]
#dataframe_filtered.drop([4,17,18,21,24,30,43],axis=0,inplace=True) #remove some unwanted locations like hotels
dataframe_filtered.drop(['country','region','locality'],axis=1,inplace=True) #no need for those columns as we know we're in Bangalore,IN
dataframe_filtered
