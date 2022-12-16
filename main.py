# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Warren Wu
#               Brooke Smith
#               Sophie Skop
#               Dylan Jacobs
# Section:      562
# Assignment:   Final Project
# Date:         6 December 2022

# doitforfishbaker
'''
Main file that creates objects of other classes
Main file also runs turtle and makes minor graphical adjustments

Team Members that contributed:
Warren (organized code)
Sophie (turtle graphics)
'''

# import libraries
import turtle
import instructions
import map
from math import *
import tkinter as tk
import importlib


def angle(x1, x2, y1, y2):
    '''
      Determines the angle between two points on the screen
      Parameters: x and y coordinates of the two points
      Returns: the angle between the two points
      '''
    if x2 - x1 == 0:  # is 180 degrees if no change in x
        return 180
    # calculate angle between the two points
    angle = atan2(y2 - y1, x2 - x1) / pi * 180
    return angle


def dist(x1, x2, y1, y2):
    '''
      Determine the distance between two points on the screen
      Parameters: x and y coordinates of the two points
      Returns: the distance between the two points
      '''
    return sqrt((y2 - y1)**2 + (x2 - x1)**2)


def distanceConverter(unit, val):
    '''
      Converts whatever unit to pixels for turtle to comprehend
      Parameter: string of the unit, value of the unit
      Returns: corresponding pixel length
      '''
    if unit == 'ft':
        val /= 5280
    return 110.7851532 / 3.17386 * val  # super secret mile to pixel converter


def main():
    # get important instruction data
    print("ADD ALL INSTRUCTION TXT TO 'instructions' FOLDER")
    print("WARNING: ENTER THE FILE NAME WITHOUT .TXT AT THE END")
    print("DON'T INPUT FILE PATH JUST FILE NAME")
    print("EXAMPLE: 'Kyle2VetPk'\n")
    userInput = input("Enter the instruction file NAME: ")
    turtle.clear()
    filePath = "Final_Project//instructions//" + userInput + ".txt"
    data = instructions.Instructions(filePath)
    driving = data.getDrivingInstructions()
    commands = data.translate(driving)
    # generate map and get important coordinates
    address = data.getAddress()
    bcs = map.Map(address)
    addressLoc = bcs.getLocation()
    bcs.generateMap(addressLoc[0], addressLoc[1])
    bcs.setBgTrans()
    bcs.setMapOverlay()
    points = bcs.getCoords()
    # assign default values
    try:
        start = points["start"]
        end = points["end"]
    except:
        start = points["end"]
        end = [705, 544]
    description = data.getLocation()
    console = data.getPrintInstructions()

    # convert to cartesian coordinates w/ a lil bit of math
    start = [(float(start[0]) - 500) - 3, -1 * (float(start[1]) - 500)]
    end = [(end[0] - 500) + 3, -1 * (end[1] - 500)]

    # initialize turtle components
    s = turtle.Screen()
    s.bgpic("Final_Project//maps//final_map.png")
    s.update()
    turtle.title("Awesome Map Program")
    t = turtle.Turtle()
    t.speed(1)
    t.width(4)

    # turtle starting animation
    # start map application

    # move to start point
    t.penup()
    t.goto(start[0], start[1])
    t.pendown()
    t.write(description[0], font=("Calibri", 16, "bold"))
    t.setheading(angle(t.xcor(), end[0], t.ycor(), end[1]))
    print("\n" + console[0] + "\n" + console[1])
    for index in range(2, len(console)):
        print(console[index])
    # loop through commands
    for command in commands:
        actions = command.split()
        # look at each action event and direct turtle accordingly
        if actions[0] == "rotate":
            t.setheading(int(actions[1]))
        elif actions[0] == "left":
            t.left(int(actions[1]))
        elif actions[0] == "right":
            t.right(int(actions[1]))
        elif actions[0] == "forward":
            distance = float(actions[1])
            distance = distanceConverter(actions[2], distance)
            t.forward(distance)

    # final graphical adjustments
    compass = angle(t.xcor(), end[0], t.ycor(), end[1])
    ruler = dist(t.xcor(), end[0], t.ycor(), end[1])
    t.setheading(compass)
    t.forward(ruler)
    t.write(description[1], font=("Calibri", 16, "bold"))
    turtle.done()


if __name__ == '__main__':
    # ;-; this project sucks
    main()
