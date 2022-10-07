import os, sys
import requests
from requests.auth import HTTPBasicAuth
import json
import geojson

# NOTE: Requires a Mapbox API key stored in the MAPBOX_API_KEY environment variable.

def get_route_instructions(start: str, end: str, api_key: str) -> list:
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving-traffic/{start};{end}" \
          f"?geometries=geojson&overview=full&steps=true&access_token={api_key}"
    response = requests.get(url)
    route = response.json()
    return route["routes"][0]["legs"][0]["steps"]

def format_route(start: str, end: str, api_key: str):
    instructions = []
    for direction in get_route_instructions(start, end, api_key):
        temp = []
        temp.append(direction["maneuver"]["instruction"])
        temp.append(direction["distance"])
        instructions.append(temp)
    return instructions

def line_to_linestring(line: str) -> geojson.LineString:
    coords = []
    for coord in line["coordinates"]:
        coords.append([float(coord[0]), float(coord[1])])
    return geojson.LineString(coords)

def format_route_geojson(start: str, end: str, api_key: str) -> list:
    route = []
    for step in get_route_instructions(start, end, api_key):
        route.append(line_to_linestring(step["geometry"]))
    return route

def plot_route(start: str, end: str, api_key: str):
    print("*** Start ***")
    # Print the formatted route in an easy-to-read format.
    for direction in format_route(start, end, api_key):
        print(direction[0])
        print(str(round((direction[1] * .000621371), 2)) + " miles")
    # Plot the route using GeoJSON provided by Mapbox.
    #for line in format_route_geojson(start, end, api_key):
    #    for coord in geojson.utils.coords(line):
    #        print('Longitude:' + str(coord[0]))
    #        print('Latitude:' + str(coord[1]))
    #    print()
    #print()
    print("*** End ***")
    #print()

if __name__ == "__main__":
    plot_route("-97.424226,35.652101", "-97.03949,37.07791", os.environ["MAPBOX_API_KEY"]) # Default route from Dallas to Fort Worth
