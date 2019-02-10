import csv
import folium
from geopy.geocoders import ArcGIS


def dic_cr(year):
    """
    (int) -> dict
    Reads csv file and makes a dictionary, where the key is location
     and value is a list of films of the year entered by user
    :param year: a year to search films entered by user
    :return:the dictionary of locations and films
    """
    lst_films = []
    dic_m = {}
    with open("locations.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lst_films.append(dict(row))
    for dic in lst_films:
        if dic.get("year") == str(year):
            if dic.get("location") != "NO DATA":
                if dic.get("location") not in dic_m:
                    dic_m[dic.get("location")] = []
                dic_m[dic.get("location")].append(dic.get("movie"))

    csvfile.close()
    return dic_m


def map_cr(dic_m):
    """
    (dict) -> None
    Builds the  html map with pointers. Pointers are the list of films.
    :param dic_m: the dictionary of locations and films
    :return: None
    """
    map = folium.Map()
    fg = folium.FeatureGroup(name="Films_map")
    for key, value in dic_m.items():
        try:
            loc = geo(key)
            fg.add_child(folium.Marker(location=loc,
                                       popup=str(value).replace("'", ""),
                                       icon=folium.Icon()))
        except:
            continue

    fg_pp = folium.FeatureGroup(name="Population")

    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                                             encoding='utf-8-sig').read(),
                                   style_function=lambda x: {'fillColor': 'green'
                                   if x['properties']['POP2005'] < 10000000
                                   else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                   else 'red'}))
    map.add_child(fg)
    map.add_child(fg_pp)
    map.add_child(folium.LayerControl())
    map.save('Map1.html')


def geo(location):
    """
    (str) -> list
    Returns the list of coordinates from locations
    :param location:
    :return: list of coordinates
    """
    geolocator = ArcGIS()
    try:
        location = geolocator.geocode(location)
        location = [location.latitude, location.longitude]
        return location
    except:
        pass


def main():
    """
    It is main function. It asks a year from user and calls other functions
    """
    year = int(input("Enter a year: "))
    dict_year = dic_cr(year)
    map_cr(dict_year)
    print("The map is ready")


main()
