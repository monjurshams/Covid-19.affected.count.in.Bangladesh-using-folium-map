# This project is on Covid-19 affected count showing on the map using Python and Folium.

	
## Image of the map:
![alt text](https://github.com/monjurshams/Practice-Projects/blob/master/Covid-19-affected-count-in-MAP/Image%20of%20map.jpg "Map of Bangladesh with the count of Covid-19 affecteds in districts")



## Features:

1. It can fetch pdf from IEDCR, Bangladesh website where the data of the affected people is updated every day. 

2. It can convert the pdf into multiple tables and csv files containing total affected counts in the entire country and Dhaka city as well.

3. It can fetch the geo locations of the districts and the areas and then show it in the map.

4. User can switch between options. He can choose either the whole country's count or only Dhaka's count.


## Shortcomings:

1. The pdf fetching can take a bit time as it depends on the internet connections, website traffics and etc.

2. Sometimes the geo codings can give a timeout message also due to internet connection and geo location's avilability.

3. This program is designed in such way that if any location's coordinate is not found, the row will be null. That causes some data to get lost, thus reducing the credibility of the map by a little margin. But it is normal as there are quite a few remote areas in the country that are not found in  the geopy library.

4. Due to the lack of well structured geojson file, choropleth or geojson polygon borders could not be added. It could be done manually by forming my own geojson file. But it would be a heavily cumbersome task to perform.

# FEEL FREE TO EXPLORE!