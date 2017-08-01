"""
Spinner class simulates a fidget spinner
@author: marcelruland

colors for lights are set by calling set_color0(), set_color1() set_color2(), which take an array of length 4 and interpret its variable as rgba value


FUTURE ADD-ONS:

high priority:
- create setter, add default parameter values, and remove mandatory parameters for:
    slowdown, slowdownspeed, jiggle, rpm

low priority:
- implement different colour modes, e.g. 'random', 'predetermined'
- redraw equilateral triangle so 30º rotation becomes obsolete
"""

wide = 800  # canvas width
high = wide / 4 * 3  # canvas height, conserves 3/4 aspect ratio
angle = 0  # initiate rotation with 0 degrees

"""play around with these variables to change behaviour (but hurry up, they'll soon be turned into methods)"""
framerate = 30  # framerate, decrease to improve performance
rpm = 300  # initial rotations per minute
slowdown = True  # if True, then fidget spinner will slowly decrease rpm
slowdownspeed = framerate / 60  # speed is decreased every n frames
if slowdownspeed <= 0:
    slowdownspeed = 1
jiggle = True  # randomness in light positions
colormode = 'random'  # set to 'random' or 'predetermined', DOES NOT WORK YET


def setup():
    global wide, high, framerate, font
    size(wide, high)
    frameRate(framerate)
    noStroke()
    rectMode(CENTER)
    font = createFont("Arial", 14, True)


class Spinner:
    
    # rows store rgba values for: 0th light, 1st light, 2nd light, body
    __colorarray = [[255, 0, 0, 255],
                    [0, 255, 0, 255],
                    [0, 0, 255, 255],
                    [128, 128, 128, 255]]
    __x = wide / 2
    __y = high / 2


    def __init__(self, radius):
        """
        constructor function
        x, y are coordinates for instance's origin
        radius is instance's radius (you don't say...)
        r, g, b, a are instance's body colour values
        """
        self.__radius = radius
        # create array for randomness in light positions if jiggle is Truenote
        self.__jigglearray = [random(-self.__radius / 5, self.__radius / 5) for i in range(3)]
    
    
    def set_coordinates(self, x, y):
        try:
            check = x / 2
        except TypeError:
            raise TypeError('In call to set_coordinates(): Parameters must be integer or float! \nx is %s' % type(x))
        try:
            check = y / 2
        except TypeError:
            raise TypeError('In call to set_coordinates(): Parameters must be integer or float! \ny is %s' % type(y))
        self.__x = x
        self.__y = y
    

    def color_verifier(self, callermethod, colorarray):
        """
        verifies rgba colour values
        noerrors boolean will be False if any test is failed
        call within color setters, callermethod is name of calling method
        valid input is an array of length 4 with floats or integers 0 ≥ n ≥ 255
        """
        noerrors = True
        if len(colorarray) != 4:
            print('ERROR in call to %s(): Array length must be 4.\nActual is %i.' % (callermethod, len(colorarray)))
            noerrors = False
        else:
            for i in range(len(colorarray)):
                if colorarray[i] < 0 or colorarray[i] > 255:
                    try:
                        raise ValueError('In call to %s(): Array entries must be four integers or floats between 0 and 255 for rgba values! \nEntry %i is %i.' % (callermethod, i, colorarray[i]))
                    except TypeError:
                        raise TypeError('In call to %s(): Array entries must be four integers or floats between 0 and 255 for rgba values! \nEntry %i is %s.' % (callermethod, i, type(colorarray[i])))
                    noerrors = False
        if noerrors == True:
            return True
        else:
            return False


    def set_bodycolor(self, bodycolorarray):
        check = self.color_verifier('set_bodycolor', bodycolorarray)
        if check is True:
            self.__colorarray[3] = bodycolorarray


    def set_color0(self, color0array):
        check = self.color_verifier('set_color0', color0array)
        if check is True:
            self.__colorarray[0] = color0array
    
    
    def set_color1(self, color1array):
        check = self.color_verifier('set_color1', color1array)
        if check is True:
            self.__colorarray[1] = color1array


    def set_color2(self, color2array):
            check = self.color_verifier('set_color2', color2array)
            if check is True:
                self.__colorarray[2] = color2array

    def get_colorarray(self):
        return self.__colorarray


    def display(self):
        """draws fidget spinner body"""
        fill(self.__colorarray[3][0], self.__colorarray[3][1], self.__colorarray[3][2], self.__colorarray[3][3])

        """calculate equilateral triangle centered at (0,0)"""
        trirada = self.__radius
        triradb = sqrt(3) / 2 * trirada
        triradc = trirada / 2
        triangle(-triradb, triradc, 0, -trirada, triradb, triradc)
        # rotate to match up triangle and ellipses
        rotate(radians(30))
        # draw three ellipses
        for i in range(3):
            rotate(radians(120))
            ellipse(self.__radius, 0, self.__radius, self.__radius)
        # draw center ellipse
        fill(0)
        ellipse(0, 0, self.__radius / 1.5, self.__radius / 1.5)
        self.decorations()  # call function to add lights


    def rotation(self):
        """translates matrix to instance's origin, calls display function and controls rotation"""
        global rpm, angle
        pushMatrix()
        translate(self.__x, self.__y)
        rotate(radians(angle))
        self.display()
        popMatrix()
        angle += framerate / 150.0 * rpm
        if slowdown == True and frameCount % slowdownspeed == 0:
            rpm = rpm * 0.999


    def decorations(self):
        for i in range(3):
            rotate(radians(120))
            # read colours from colorarray
            fill(self.__colorarray[i][0], self.__colorarray[i][
                 1], self.__colorarray[i][2], self.__colorarray[i][3])
            # enable randomness in light positions
            if jiggle == True:
                ellipse(self.__jigglearray[i] + self.__radius,
                        0, self.__radius / 3, self.__radius / 3)
            else:
                ellipse(self.__radius, 0, self.__radius / 3, self.__radius / 3)


    def debug(self):
        """draws a wide rectangle to make rotation visible"""
        fill(self.__bodycolor[0], self.__bodycolor[1], self.__bodycolor[2], self.__bodycolor[3])
        rect(0, 0, width / 2, width / 160)


fspinner = Spinner(random(20, 400)) # create fidget spinner object with random radium
fspinner.set_coordinates(random(0, wide), random(0, high)) # randomly set coordinates of spinner

# random colours for body and all three lights
fspinner.set_color0([random(0, 255), random(0, 255), random(0, 255), 255])
fspinner.set_color1([random(0, 255), random(0, 255), random(0, 255), 255])
fspinner.set_color2([random(0, 255), random(0, 255), random(0, 255), 255])
fspinner.set_bodycolor([random(0, 255), random(0, 255), random(0, 255), 255])


def draw():
    global font
    background(0, 0, 00)  # black background
    fspinner.rotation()  # call rotation function

    """info in bottom left screen corner"""
    textFont(font)
    fill(255)
    text('Framerate:  target %.2f; actual %.2f      Rotations per Minute: %.2f' % (
        framerate, frameRate, rpm), 5, height - 5)