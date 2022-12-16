'''
Creates map object that creates the map that's going to be used as the background
Uses a couple of libraries to graphically locate known addresses within BCS area
Used image processing to convert graphically data to image data (in matrix forms)

Team Members that contributed: 
Warren (image processing)
Brooke (map selection)
'''
# doitforfishbaker


from geopy.geocoders import Nominatim  # pip install geopy
import pandas as pd  # pip install pandas
import geopandas as gpd  # pip install geopandas and dependencies
from PIL import Image  # pip install pillow
import matplotlib.pyplot as plt


class Map(object):
    def __init__(self, addresses):
        '''
        Initialization function for Map class
        Parameters: self class instance, list of addresses
        Returns: None
        '''
        self.addresses = addresses

    def generateMap(self, start, end):
        '''
        Generates map of the BCS area and saves it as map.png
        Parameters: self class instance, the start and ending coordinates as points
        Returns: None
        '''
        try:
            texas = gpd.read_file(
                'Final_Project//texas_cities_shapes//tl_2017_48_place.shp')
            bcsData = texas[texas['NAME'].isin(['College Station', 'Bryan'])]
            bcsArea = bcsData.boundary.plot(
                figsize=(10, 10), edgecolor='black')
            dfStart = pd.DataFrame(
                {'Longitude': [start[0]], 'Latitude': [start[1]]})
            dfEnd = pd.DataFrame({'Longitude': [end[0]], 'Latitude': [end[1]]})
            pointStart = gpd.GeoDataFrame(
                dfStart, geometry=gpd.points_from_xy(dfStart.Longitude, dfStart.Latitude))
            pointEnd = gpd.GeoDataFrame(
                dfEnd, geometry=gpd.points_from_xy(dfEnd.Longitude, dfEnd.Latitude))
            pointStart.plot(ax=bcsArea, color="red")
            pointEnd.plot(ax=bcsArea, color="blue")
            plt.axis('off')
            plt.grid(False)
            plt.savefig("Final_Project//maps//map.png")
        except:
            print("Error generating map.png")

    def getLocation(self):
        '''
        Get inital and final destination coordinates and plot as list of tuples
        Parameters: self class instance
        Returns: List of tuples with longitude and latitude of two addresses
        '''
        try:
            start, end = self.addresses[0], self.addresses[-1]
            geolocator = Nominatim(user_agent="102FinalAPP")
            startPoint = geolocator.geocode(start)
            endPoint = geolocator.geocode(end)
            return [(startPoint.longitude, startPoint.latitude), (endPoint.longitude, endPoint.latitude)]
        except:
            print("Error retrieving coordinates of starting point and destination")
            start = self.addresses[0].split(",")
            start = " ".join(start[1:])
            end = self.addresses[-1].split(",")
            end = " ".join(end[1:])
            geolocator = Nominatim(user_agent="102FinalAPP")
            startPoint = geolocator.geocode(start)
            endPoint = geolocator.geocode(end)
            return [(startPoint.longitude, startPoint.latitude), (endPoint.longitude, endPoint.latitude)]

    def getCoords(self, imgPath="Final_Project//maps//final_map.png"):
        '''
        Gets the pixel coordinates of starting and ending points on final map
        Parameters: image path to finalized map
        Returns: pixel coordinates of start and ending points
        '''
        try:
            imgMap = Image.open(imgPath)
            redCheck, blueCheck = False, False
            imgWidth, imgHeight = imgMap.size[0], imgMap.size[1]
            locationPixel = {}
            for row in range(imgWidth):
                for col in range(imgHeight):
                    if imgMap.load()[row, col] == (255, 0, 0, 255) and not redCheck:
                        locationPixel["start"] = [row, col]
                        redCheck = True
                    if imgMap.load()[row, col] == (0, 0, 255, 255) and not blueCheck:
                        locationPixel["end"] = [row, col]
                        blueCheck = True
            return locationPixel
        except:
            print("Error getting pixel coordinates of starting and ending points")

    def setBgTrans(self, imgPath="Final_Project//maps//map.png"):
        '''
        Make image in imgPath have a transparent background (only detects color white) and saves as map.png
        Parameters: image path in local storage
        Returns: None
        '''
        try:
            imgMap = Image.open(imgPath)
            mapColor = imgMap.convert("RGBA")
            newColor = []
            for color in mapColor.getdata():
                # looks at rgb values and changes opacity (if white then change to transparent)
                if color[0] == 255 and color[1] == 255 and color[2] == 255:
                    newColor.append((255, 255, 255, 0))
                else:  # otherwise keep the original color
                    newColor.append(color)
            mapColor.putdata(newColor)
            mapColor.save("Final_Project//maps//map.png", "PNG")
        except:
            print("Error setting image background to transparent")

    def setMapOverlay(self, mapPath="Final_Project//maps//map.png", overlayPath="Final_Project//maps//map_overlay.png"):
        '''
        Overlay map image with map overlay and saves it as final_map.png
        Parameters: path to map, path to map overlay
        Return: None
        '''
        try:
            # first store image data as variables
            imgMap = Image.open(mapPath)
            imgMapOverlay = Image.open(overlayPath)
            # resize image so overlaying doesn't look funky
            imgMapOverlay = imgMapOverlay.resize(imgMap.size)
            imgMapOverlay.paste(imgMap, (0, 0), mask=imgMap)
            imgMapOverlay.save("Final_Project//maps//final_map.png")
        except:
            print("Error pasting map overlay")
