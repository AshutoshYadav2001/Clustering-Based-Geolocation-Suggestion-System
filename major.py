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

#define coordinates of the college
map_bang=folium.Map(location=[12.971599,77.594566],zoom_start=12)
# instantiate a feature group for the incidents in the dataframe
locations = folium.map.FeatureGroup()

latitudes = list(dataframe_filtered.lat)
longitudes = list( dataframe_filtered.lng)
labels = list(dataframe_filtered.name)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup=label).add_to(map_bang)

# add incidents to map
map_bang.add_child(locations)

# add incidents to map
map_bang.add_child(locations)

map_bang

df_evaluate=dataframe_filtered[['latitude','longitude']]

import requests
import pandas as pd
from pandas.io.json import json_normalize

RestList = []
latitudes = list(dataframe_filtered.latitude)
longitudes = list( dataframe_filtered.longitude)
for lat, lng in zip(latitudes, longitudes):
    latii=lat#Query for the apartment location in question
    longii=lng

    url = "https://api.foursquare.com/v3/places/search?query=Restaurant%2CCafe&ll={},{}&radius=2000&limit=50".format(latii,longii)

    headers = {
        "accept": "application/json",
        "Authorization": "fsq3bwgrZ8jL2HXYqHqSAsg5REy1ti8FL7rFKjyCKovI3TQ="
    }

    # Now, we pull the results of the query into a json file.
    response = requests.get(url, headers=headers)
    data = response.json()
    places = data['results']
    # transform results into a dataframe
    dataframe2 = json_normalize(places)
    #dataframe2

    filtered_columns = ['name', 'categories'] + [col for col in dataframe2.columns if col.startswith('location.')] + ['geocodes.main.latitude', 'geocodes.main.longitude','fsq_id','distance']
    dataframe_filtered2 = dataframe2.loc[:, filtered_columns]
    dataframe_filtered2['categories'] = dataframe_filtered2.apply(get_category_type, axis=1)

    # clean column names by keeping only last term
    dataframe_filtered2.columns = [column.split('.')[-1] for column in dataframe_filtered2.columns]
    #dataframe_filtered.drop([4,17,18,21,24,30,43],axis=0,inplace=True) #remove some unwanted locations like hotels
    #dataframe_filtered2.drop(['country','region','locality'],axis=1,inplace=True) #no need for those columns as we know we're in Dehradun,IN
    RestList.append(dataframe_filtered2['categories'].count())

dataframe_filtered2

RestList

df_evaluate['Restaurants']=RestList

import requests
import pandas as pd
from pandas.io.json import json_normalize

FruitList = []
latitudes = list(dataframe_filtered.latitude)
longitudes = list( dataframe_filtered.longitude)
for lat, lng in zip(latitudes, longitudes):
    latii=lat#Query for the apartment location in question
    longii=lng

    url = "https://api.foursquare.com/v3/places/search?query=Fruit%2C%20Juice&ll={},{}&radius=4000&limit=50".format(latii,longii)

    headers = {
        "accept": "application/json",
        "Authorization": "fsq3bwgrZ8jL2HXYqHqSAsg5REy1ti8FL7rFKjyCKovI3TQ="
    }

    # Now, we pull the results of the query into a json file.
    response = requests.get(url, headers=headers)
    data = response.json()
    places = data['results']
    # transform results into a dataframe
    dataframe3 = json_normalize(places)
    #dataframe3

    filtered_columns = ['name', 'categories'] + [col for col in dataframe3.columns if col.startswith('location.')] + ['geocodes.main.latitude', 'geocodes.main.longitude','fsq_id','distance']
    dataframe_filtered3 = dataframe3.loc[:, filtered_columns]
    dataframe_filtered3['categories'] = dataframe_filtered3.apply(get_category_type, axis=1)

    # clean column names by keeping only last term
    dataframe_filtered3.columns = [column.split('.')[-1] for column in dataframe_filtered3.columns]
    #dataframe_filtered.drop([4,17,18,21,24,30,43],axis=0,inplace=True) #remove some unwanted locations like hotels
    #dataframe_filtered2.drop(['country','region','locality'],axis=1,inplace=True) #no need for those columns as we know we're in Dehradun,IN
    FruitList.append(dataframe_filtered3['categories'].count())

dataframe_filtered3

df_evaluate['Fruits,Vegetables,Groceries']=FruitList

df_evaluate

kclusters = 3

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(df_evaluate)
df_evaluate['Cluster']=kmeans.labels_
df_evaluate['Cluster']=df_evaluate['Cluster'].apply(str)
df_evaluate

#define coordinates of the college
map_bang=folium.Map(location=[30.41,77.96],zoom_start=12)
# instantiate a feature group for the incidents in the dataframe
locations = folium.map.FeatureGroup()
# set color scheme for the clusters
def color_producer(cluster):
    if cluster=='1':
        return 'green'
    elif cluster=='0':
        return 'orange'
    else:
        return 'red'
latitudes = list(df_evaluate.latitude)
longitudes = list(df_evaluate.longitude)
labels = list(df_evaluate.Cluster)
names=list(dataframe_filtered.name)
for lat, lng, label,names in zip(latitudes, longitudes, labels,names):
    folium.CircleMarker(
        [lat,lng],
        fill=True,
        fill_opacity=1,
        popup=folium.Popup(names, max_width = 300),
        radius=5,
        color=color_producer(label)
    ).add_to(map_bang)

# add locations to map
map_bang.add_child(locations)

map_bang
