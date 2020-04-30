#!/usr/bin/env python
# coding: utf-8

# ###
# Importing the necessary libraries for the project
# Folium = To show the map
# Pandas = To fit the dataset into a dataframe for ease
# Tabula & Camelot = To read the pdf dataset {Tabula Need Java8+ installed on the pc } {Both of their function is same while camelot can give extra benifit in case of any utf-8 errors occur}
# Geopy,Nominatim = For fetching the geo location codes i.e Coordinates of the Locations
# ###

# In[2]:


import folium
import pandas as pd
import tabula
from geopy.geocoders import Nominatim
nom=Nominatim(user_agent="Covid-19 affected count in MAP", scheme="http",timeout = 5)


# ###
# Converting the pdf into two csv files, one for the whole country's affected count district-wise 
# and the other one is for only Dhaka's affected count area-wise
# Here I used camelot to read the first table of the first page, tabula for the second page. This is just for exploring multiple functions.
# ###

# In[3]:


file  = "https://www.iedcr.gov.bd/website/images/files/nCoV/Case_distribution_24_April_update.pdf"
tables = tabula.read_pdf(file, pages = "all", multiple_tables = True)
tables = camelot.read_pdf(file, pages = "1")
tables[0].to_csv("Country_Count.csv")
tabula.convert_into(file, "Dhaka_Count.csv", pages = '2')


# ###
# Starting to clean up the dataset, first we import it and use pandas dataframe to read the csv file.
# Then I dropped the unnecessary coloumns.
# Afterwards, I added "Bangladesh" after each location so that it becomes easier to find the location's coordinates
# ###

# In[4]:


country_count = pd.read_csv("Country_Count.csv")
country_count=country_count.drop(["Division","Division.1","%"],1)
country_count["District/City"] = country_count["District/City"] + "," + "Bangladesh"


# ###
# Now, I fetched the coordinates of the districts using nominatim library from server and added it to an extra column named "Coordinates"
# ###

# In[5]:


country_count["Coordinates"] = country_count["District/City"].apply(nom.geocode)


# ###
# After that, I dropped the columns that nominatim failed to fetch the coordinates to clean the dataset. 
# Then I fetched the Latitudes and Longitudes of the districts from the coordinates and add them in separate columns.
# ###

# In[6]:


country_count=country_count.dropna()
country_count["Latitude"] = country_count["Coordinates"].apply(lambda x: x.latitude)
country_count["Longitude"] = country_count["Coordinates"].apply(lambda x: x.longitude)


# ###
# Finally, I plotted the map with folium. First I created some necessary variables containing the latitude,longitude and total affected numbers.
# Then I created an object of folium's map class with a base location. In this case, the base location is Bangladesh's coordinates.
# I passed 3 variables in a for loop. The lat, lon and the total number of affected.
# Then I have used a feature of folium which is circle marker to mark the locations in the map. 
# Inside the marker function, I added the feature 'popup' to show the number of the affected on click. 
# For convinience, I created a feature group and then added the features as a child of this group.
# After that, I added the feature group to the map object of folium and then saved the map.
# ###

# In[14]:


lat_country = list(country_count["Latitude"])
lon_country = list(country_count["Longitude"])
total_country = list(country_count["Total"])
Map = folium.Map(location =[23.6850,90.3563],zoom_start = 7)
f_group_country = folium.FeatureGroup(name="Country Count")
for lt,ln,total in zip(lat_country,lon_country,total_country):
    f_group_country.add_child(folium.CircleMarker(location = [lt,ln], popup="Affected: "+str(total_country),radius=8, fill_color='red',color='grey',fill_opacity=1))


# ##
# Following is the code for dhaka_count. It is almost same, with some little differences.
# ##

# In[8]:


dhaka_count = pd.read_csv("Dhaka_Count.csv")
dhaka_count["Location"] = dhaka_count["Location"] + "," + "Dhaka"+ "," + "Bangladesh"


# In[9]:


dhaka_count["Coordinates"] = dhaka_count["Location"].apply(nom.geocode)


# In[10]:


dhaka_count = dhaka_count.dropna()
dhaka_count["Latitude"] = dhaka_count["Coordinates"].apply(lambda x: x.latitude)
dhaka_count["Longitude"] = dhaka_count["Coordinates"].apply(lambda x: x.longitude)


# ###
# This is almost same as the previous function mentioned above for the country's count. Only difference is that I added the two features in different feature group and here the base map is only Dhaka's map.
# So that I can add them in a layer control of folium. Thus we can switch between the options.
# ###

# In[15]:


lat_dhaka = list(dhaka_count["Latitude"])
lon_dhaka = list(dhaka_count["Longitude"])
total_dhaka = list(dhaka_count["Total"])
f_group_dhaka = folium.FeatureGroup(name="Dhaka Count")
for lt_dhaka,ln_dhaka,total_dhaka in zip(lat_dhaka,lon_dhaka,total_dhaka):
    f_group_dhaka.add_child(folium.CircleMarker(location = [lt_dhaka,ln_dhaka], popup="Affected: "+str(total_dhaka),radius=10, fill_color='red',color='grey',fill_opacity=1))

Map.add_child(f_group_country)
Map.add_child(f_group_dhaka)
Map.add_child(folium.LayerControl())
Map.save("Corona affected count Map for Bangladesh.html")


# Backup code in case any malfunction occurs while fetching the coordinates[except timeout]:
#     Sometimes there can be error while finding some locations with geopy. To see which particular location is causing the error, I wrote this loop with try-except which will find the coordinates one by one unlike the method that I used above. And if there is any error, you can find exactly which location it is failing to fetch.
#     
# ###Backup code
# 
# for address in country_count["District/City"]:
#     try:
#         gcode=nom.geocode(str(address))
#         print("Latitude of the %s is: " %address, gcode.latitude)
#     except:
#         print("I can't find the coordinates of %s" %address)

# In[ ]:




