'''
Instructions object that takes data from instruction file outputs relevant data
Designed to take keywords and give meaning to numbers
Tested with a variety of different inputs to ensure accurate and reliable instructions

Team Members that contributed:
Warren (organizing code and getAddress() function)
Dylan (data cleaning and choosing keywords)
'''
# doitforfishbaker


class Instructions(object):
    def __init__(self, fileID):
        '''
        Initialization function for Instructions class
        Parameters: self class instance, file path to instructions
        Returns: None
        '''
        self.fileID = fileID

    def getPrintInstructions(self):
        '''
        Gets the instructions that are going to be printed
        Parameters: self class instance
        Returns: Instructions to be printed
        '''
        data = []
        with open(self.fileID) as f:
            for line in f:
                line = line.strip()
                data.append(line)
        return data

    def getDrivingInstructions(self):
        '''
        Gets the keywords and units from direction file
        Paramters: self class instance
        Returns: Instructions in form of keywords
        '''
        distance = ["ft", "feet", "mi", "miles"]
        direction = ["slight left", "left", "right", "northwest", "northeast",
                     "southeast", "southwest", "north", "south", "east", "west"]
        driving = []
        data = ""
        with open(self.fileID) as f:
            data = f.read()
        data = data.split("\n")
        data = data[3:-2]
        counter = 0
        for line in data:
            line = line.lower()
            if line == "":
                continue
            if counter % 2 == 0:  # looks at direction line
                if "stay" in line:
                    counter += 1
                    continue
                for unit in direction:
                    if unit in line:
                        driving.append(unit)
                        break
                counter += 1
            else:  # looks at distance line
                if line[0] == " ":
                    continue
                for unit in distance:
                    if unit in line:
                        tempIndex = line.rfind(unit, 0, len(line))
                        if tempIndex == -1:
                            continue
                        driving.append(
                            line[tempIndex-4:tempIndex-1] + " " + unit)
                        break
                counter += 1
        return driving

    def getAddress(self):
        '''
        Gets the address of the starting and ending points
        Parameters: self class instance
        Returns: List of the start and ending address
        '''
        data = []
        with open(self.fileID) as f:
            data = f.readlines()
        data = [data[1].strip(), data[-1].strip()]
        return data

    def getLocation(self):
        '''
        Gets the location information of the starting and ending points
        Parameters: self class instance
        Returns: List of where the start and end points are
        '''
        data = []
        with open(self.fileID) as f:
            data = f.readlines()
        data = [data[0].strip(), data[-2].strip()]
        return data

    def translate(self, drivingInstructions):
        '''
        Translates from human driving instructions to organized instructions for turtle
        Parameters: self class instance, human driving instruction list
        Returns: List of more organized data points and isntructions to feed to turtle
        '''
        direction = {"slight left": 20, "left": 90, "right": 90, "northwest": 135, "northeast": 45,
                     "southeast": 315, "southwest": 225, "north": 90, "south": 270, "east": 0, "west": 180}
        distance = ["mi", "miles", "ft", "feet"]
        translated = []
        for command in drivingInstructions:
            temp = False
            for units in direction:
                if "slight left" in command:
                    translated.append("left"+" "+str(direction["slight left"]))
                    temp = True
                    break
                if "left" in command:
                    translated.append("left"+" "+str(direction["left"]))
                    temp = True
                    break
                if "right" in command:
                    translated.append("right"+" "+str(direction["right"]))
                    temp = True
                    break
                elif units in command:
                    translated.append("rotate "+str(direction[units]))
                    temp = True
                    break
            if not temp:
                for units in distance:
                    if units in command:
                        translated.append("forward "+command)
        return translated
