import Draw
import random
import math

#get started with global variables: 

#canvas width and height 
CANVAS_WIDTH = 1000 
CANVAS_HEIGHT = 750 

#x, y location and width for the segment bar
SEGMENT_BAR_X = 165 
SEGMENT_BAR_WIDTH = 215   #segment bar goes from 165 - 380
SLIDER_Y = 533 

#x,y location and width for the angle bar 
ANGLE_BAR_X = 570 
ANGLE_BAR_WIDTH = 330  #angle bar goes from 570 - 900 

#the clicking range / the min and max for the segment bar.  
#the min value is 10 to the left of the segment bar to give clicker wiggle room 
#the max value is 2 less than the rightmost value of the bar because don't want 
#the segment knob to go off the bar. 
SEGMENT_CLICK_MIN = SEGMENT_BAR_X - 10                    #155
SEGMENT_CLICK_MAX = SEGMENT_BAR_X + SEGMENT_BAR_WIDTH -2  #378

#the clicking range / the min and max for the angle bar 
ANGLE_CLICK_MIN = ANGLE_BAR_X - 10                    #560
ANGLE_CLICK_MAX = ANGLE_BAR_X + ANGLE_BAR_WIDTH - 2   #898

# coordinates for the color buttons that are the same for each. 
COLOR_BOX_Y = 625
COLOR_BOX_WIDTH = 90 
COLOR_BOX_HEIGHT = 30

#the x location for each color button, each button is 92 pixels away from the other 
BLUEBOX_X = 220
CYCLEBOX_X = BLUEBOX_X + COLOR_BOX_WIDTH + 2   #312 
SEGBOX_X = CYCLEBOX_X + COLOR_BOX_WIDTH + 2    #404 


#the x,y width, height for the black display screen 
DISPLAY_X = 150 
DISPLAY_Y = 100 
DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 400 

#the center of the black display screen 
CENTER_DISPLAY_X = (DISPLAY_X + (DISPLAY_X + DISPLAY_WIDTH)) /2  #500
CENTER_DISPLAY_Y = (DISPLAY_Y + (DISPLAY_Y + DISPLAY_HEIGHT)) /2 #300 


#list with background options for color. used for color of "color" buttons 
#and will be used for the color of line segments. 15 total 
COLOR_LIST = [Draw.ORANGE, Draw.BLUE, Draw.WHITE, Draw.MAGENTA, Draw.GREEN, 
              Draw.CYAN, Draw.RED, Draw.YELLOW, Draw.DARK_BLUE, Draw.VIOLET,
              Draw.PINK, Draw.DARK_RED, Draw.DARK_GREEN, Draw.LIGHT_GRAY, Draw.DARK_GRAY]


#helper functions: 

#function that converts where the mouse is on either segment or angle bar 
#from knob position that was found in user() to a value that is suitable 
#to be passed in drawBoard() and drawSpirio() 
#takes in, the max and min clicking range, where the click was and how many 
#sections does the bar need to be divided into 

def convert(click_max, click_min, click, sections): 
    
    #find the clicking range 
    click_range = click_max - click_min 
    
    #how big each section is based on the clicking range 
    section_width = click_range / sections 
    
    #subtract to find how far from the leftmost value is the click. 
    #then integer divide that value by the width of each section
    #to find what number it converts to. +1 bc integer division starts at 0 
    num = int(((click - click_min) // (section_width) +1))
    
    #protection to keep value between 1- section 
    above_zero = max(1, num) 
    num = min(sections, above_zero) 
    
    #return converted number 
    return num 

#function that takes points from when drawSpiro= False. and makes
#them into the nice beautiful numbers by scaling and transofrming them 
#so that the when drawSpiro is actually drawn it's centered and scaled. 
#takes as parameters the raw x and y of drawSpiro, and then center of the 
#spiro before transformed and the scale 
#function gets called in drawSpiro() 
def cleanUp(x1, y1, x2, y2, centerX, centerY, scale): 
    
    
    #first scale and transform the currentX and currentY by: 
    #1. move spiro so its center is at (0,0) in theory 2. scale it to fit display
    #3. put that shape into the display center
    plotX1 = (x1-centerX) / scale + CENTER_DISPLAY_X
    plotY1 = (y1 - centerY) / scale + CENTER_DISPLAY_Y
    
    #do the same for the nextX and nextY 
    plotX2 = (x2-centerX) / scale + CENTER_DISPLAY_X
    plotY2 = (y2 - centerY) / scale + CENTER_DISPLAY_Y
    
    return plotX1, plotY1, plotX2, plotY2
   

       
#function to see if next x and y are within small range of the initial points 
#heading in the same direction meaning the shape is closed. 
#to be used in drawspiro function
def closeToStart(initialX, initialY, nextX, nextY, initialAngle, currentAngle): 
    
    #checks the difference between the next X and Y and the initial. 
    #equals true if it meets the requirements
    if abs(initialX - nextX) <= 0.5 and abs(initialY - nextY) <= 0.5: 
        position_close = True 
    else: position_close =  False 
     
    #checks the difference between the angle and the starting angle. 
    #equals true if it meets the requirements 
    if abs(initialAngle - currentAngle) <= 0.01 : 
        angle_close = True 
    else: angle_close = False  
    
    # if both meet the conditions it returns True, else it returns False
    return position_close and angle_close


#background design functions: 

#function to set up background 
def background(): 
    #blue background 
    Draw.setBackground(Draw.DARK_BLUE)   
    
    #white screen on top of blue
    Draw.setColor(Draw.WHITE)
    Draw.filledRect(30,30,940,690)
    
    #black display sreen on top 
    Draw.setColor(Draw.BLACK)
    Draw.filledRect(DISPLAY_X,DISPLAY_Y,DISPLAY_WIDTH,DISPLAY_HEIGHT)
    
    #setup for title "spriolateral generator"
    Draw.setFontSize(50)
    #Draw.setFontFamily("Courier")
    Draw.setColor(Draw.DARK_BLUE)
    Draw.string("SPIROLATERAL GENERATOR", 165, 40)    

#set up slider bars and knobs 
def sliders(segment_knob, angle_knob): 
    #set up for segment slider and agle slider 
    
    #text "segments" and "angles" next to the slider 
    Draw.setColor(Draw.DARK_BLUE) 
    Draw.setFontSize(22)
    Draw.string("Segments: ", SEGMENT_BAR_X - 130, 524)
    Draw.string("Angles: ", ANGLE_BAR_X - 100, 524)    
    
    #gray slider box for segment and angle 
    Draw.setColor(Draw.GRAY)
    Draw.filledRect(SEGMENT_BAR_X,SLIDER_Y,SEGMENT_BAR_WIDTH,10)
    Draw.filledRect(ANGLE_BAR_X,SLIDER_Y,ANGLE_BAR_WIDTH,10)
    
    #set up black circle to move on both sliders 
    Draw.setColor(Draw.BLACK)
    Draw.filledOval(segment_knob, SLIDER_Y - 5, 20, 20)
    Draw.filledOval(angle_knob, SLIDER_Y - 5, 20, 20)
    
    #convert the  user click on segment bar from a number between 1-15 
    segment_num = convert(SEGMENT_CLICK_MAX, SEGMENT_CLICK_MIN, segment_knob, 15)
    
    #covert the user click on angle from a number between 1-179
    angle_num = convert(ANGLE_CLICK_MAX, ANGLE_CLICK_MIN, angle_knob, 179)


    #text on the right of each slider for segment value and angle value 
    Draw.string(segment_num, SEGMENT_CLICK_MAX + 22, 525)
    Draw.string(angle_num, ANGLE_CLICK_MAX + 22, 525)      
    
    return segment_num, angle_num 

#set up colo buttons 
def color_button(color_click): 
    #set up boxes where to select color
    Draw.setFontSize(28)
    Draw.setColor(Draw.DARK_BLUE) 
    Draw.string("Color: ", 120, 625)    
    
    #the selected button becomes blue and the other button stay dark blue 
    
    blueBox_color = COLOR_LIST[1] if color_click ==  "blue" else COLOR_LIST[8]
    cycleBox_color = COLOR_LIST[1] if color_click == "cycle" else  COLOR_LIST[8]
    segBox_color = COLOR_LIST[1] if color_click == "segment" else  COLOR_LIST[8]     
        
    #draw blue button
    Draw.setColor(blueBox_color)
    Draw.filledRect(BLUEBOX_X, COLOR_BOX_Y, COLOR_BOX_WIDTH, COLOR_BOX_HEIGHT)
    
    #draw cycle button
    Draw.setColor(cycleBox_color)
    Draw.filledRect(CYCLEBOX_X, COLOR_BOX_Y, COLOR_BOX_WIDTH, COLOR_BOX_HEIGHT) 
    
    #draw segment button
    Draw.setColor(segBox_color)
    Draw.filledRect(SEGBOX_X, COLOR_BOX_Y, COLOR_BOX_WIDTH, COLOR_BOX_HEIGHT)

    # text within each box 
    Draw.setColor(Draw.WHITE) 
    Draw.setFontSize(18)
    Draw.string("Blue", 245, 632)
    Draw.string("Cycle", 330, 632)
    Draw.string("Segment", 409, 632)

def random_button(): 
    # random button
    Draw.setColor(Draw.DARK_BLUE) 
    Draw.filledRect(600, 600, 240, 80)    
    Draw.setColor(Draw.WHITE)
    Draw.setFontSize(18)
    Draw.string("Click here for", 640, 615)
    Draw.string("random spirolateral!", 615, 630)    


#this function calls DrawSpiro without actually drawing anything and finds
#info for cycles, max/min for center and sclaing 
#based on the info from this we put it into the drawSpiro when the shape
#is actualy drawn 
def testRuns(segment_knob, angle_knob, color_click): 
    slide_knob = sliders(segment_knob, angle_knob) 
    segment_num, angle_num = slide_knob 
    
    #this checks to see if the spiro closes or not because the max possible cycles 
    #needed for a spiro to close is 360. so if it goes more than 360 cycles
    #it is an unclosed cycle, in which case I want to stop it at 5 cycles 
    
    #run drawSpiro() without drawing, to find if spiro went over 360 cycles 
    cycleMax = 361
    cycleAns = drawSpiro(segment_num, angle_num, color_click, cycleMax, draw=False) 
    
    maxX, minX, maxY, minY, cycle_count = cycleAns 
    
    #if the spiro was unclosed then run it again, but stopping it at 5 cycles. 
    #use the information from this run to find the min and max of x,y 
    if cycle_count == 361: 
        cycle_num = 5 
        results = drawSpiro(segment_num, angle_num, color_click, cycle_num, draw=False) 
    
    #if it does close, then set the spiro to stop at 360 cycles   
    else: 
        cycle_num = 360
        results = drawSpiro(segment_num, angle_num, color_click, cycle_num, draw=False)
    
    #unpack tuple 
    maxX, minX, maxY, minY, cycle_count = results 

    
    #Compute centerX and centerY
    centerX = (maxX + minX) / 2 
    centerY = (maxY + minY) / 2
    
    #how wide and tall is the raw sprio 
    width = maxX - minX
    height = maxY - minY
    
    #the scaling for the x and y to fit the display screen 
    scaleX = width/DISPLAY_WIDTH
    scaleY = height/ DISPLAY_HEIGHT
    
    #chose the larget scale value so that both fit 
    if scaleX >= scaleY: 
        scale = scaleX
    else: 
        scale = scaleY
    
    # change scale to make the shape smaller so that it's not pressed against the edge. 
    #for unclosed spiro, making sure nothing sticks out of 
    #the display screen 
    if cycle_num == 5: 
        scale /= 0.7 
    else:    
        scale /= 0.94
    
    #this to be passed in the final drawSpiro call 
    return segment_num, angle_num, cycle_num, centerX, centerY, scale
    
    

def drawBoard(segment_knob, angle_knob, color_click,): 
    
    Draw.clear()
    
    #call functions to set up the screen 
    background() 
    
    color_button(color_click)
    
    random_button()
    
    #call drawSPiro without running it to find what paramerters need to be 
    #passed in when it actually gets drawn 
    final = testRuns(segment_knob, angle_knob, color_click) 
    segment_num, angle_num, cycle_num, centerX, centerY, scale = final

    #call drawSpiro() with updates values so that there is a new center and scale 
    #that info is needed for cleanUp() which is called in drawSpiro() 
    #this time the spirolateral will actually be drawn! 
    drawSpiro(segment_num, angle_num, color_click, cycle_num, centerX, centerY, scale, draw = True) 
    
    Draw.show() 
    

#function that does the calcuations to for the spiro to be drawn 
def drawSpiro(segment_num, angle_num, color_click, cycle_num, centerX = CENTER_DISPLAY_X, centerY = CENTER_DISPLAY_Y, scale = 1, draw = True):
    
    #starting angle in radians. 
    #also convert it from the turning angle to the interior angle 
    angleRad = (180 - angle_num) * (math.pi / 180) 
    
    #starting points are the midpoint of black plot graph. value doesn't change 
    initialX = CENTER_DISPLAY_X
    initialY = CENTER_DISPLAY_Y
    
    #variables to track the current values of x,y,angle. these change in the loop
    currentX = initialX 
    currentY = initialY 
    currentAngle = angleRad     
    
    #start nextX and nextY at zero, random number so that closeToStart starts as false 
    nextX = 0 
    nextY = 0     
    
    #initial values for max and min at the lowest and highest values, respectively 
    maxX = -float("inf")
    minX =  float("inf")
    maxY = -float("inf")
    minY =  float("inf")        
    
    #cycle counter 
    cycle_count = 0 
    
    #cycle loop. falls out of loop when close to start returns true or if there has been more than 360 cycles 
    while not closeToStart(initialX, initialY, nextX, nextY, angleRad, currentAngle) and cycle_count < cycle_num: 
        
        #now loop through each segment in the cycle 
        for i in range(1, segment_num+1): 
            
            #length of line, each segment goes up by 1 
            length=  i 
            
            #2nd set of points in the line 
            nextX =  currentX + length * math.cos(currentAngle) 
            nextY =  currentY - length * math.sin(currentAngle)  
            
            
            #if not anything be drawn just trying to find the min,max,center
            if draw == False:
                
                #checks point to see if they should be the current min/max 
                if currentX > maxX:
                    maxX = currentX
                if currentX < minX:
                    minX = currentX
                if currentY > maxY:
                    maxY = currentY
                if currentY < minY:
                    minY = currentY                
                
            #if   the spiro is actaully being drawn: 
            if draw == True: 
                
                #determines color of line 
                if color_click == "blue":
                    Draw.setColor(Draw.BLUE) 
                elif color_click == "segment": 
                    Draw.setColor(COLOR_LIST[i-1])
                elif color_click == "cycle": 
                    Draw.setColor(COLOR_LIST[cycle_count%15])                
                
                #finds the scaled and centered of the first 2 points in the line
                #using cleanUP 
                Points = cleanUp(currentX, currentY, nextX, nextY, centerX, centerY, scale) 
                x1, y1, x2, y2 = Points 
                
                #draws the line segment 
                Draw.line(x1, y1, x2, y2) 
            
                
            #update x and y from 2nd point of first line to 1st point on the
            #next line 
            currentX = nextX 
            currentY = nextY
                
            #update current angle to change direection 
            #and makes sure it stays in between 0-2pi 
            currentAngle = (currentAngle + angleRad) % (2 * math.pi)                   
                
            
        #add 1 to cycle count     
        cycle_count += 1
    
    #if in first call of drawSpiro() return tuple with the min/max of x, y    
    if draw == False: 
        return maxX, minX, maxY, minY, cycle_count 


#function to determnine how the spirolateral should be drawn based on user clicks 
def user(): 
    
    #start off at the initial value so that if nothing gets clicked, stays the same
    segment_knob = 265 
    angle_knob = 672
    color_click = "blue" 
    
    #draggers start at false 
    segment_slide = False 
    angle_slide = False 
    
    
    #infinite loop! 
    while True:
             
        #check if there was any mouse action 
        #new variables assigned to x,y value of where there was mouse action 
        if Draw.mousePressed():
            newX = Draw.mouseX()
            newY = Draw.mouseY() 
            
            #if left click 
            if Draw.mouseLeft():
            
                #if clicks in random button 
                if newX >= 600 and newX <= 840 and newY >= 600 and newY <= 680:
                    
                    #radonly assign segment and angle to a value 
                    #within their min and max 
                    segment_knob = random.randint(SEGMENT_CLICK_MIN,SEGMENT_CLICK_MAX) 
                    angle_knob = random.randint(ANGLE_CLICK_MIN,  ANGLE_CLICK_MAX)
                    
                    
                   
                    
                #if clicked color boxes- is it in y value range of the boxes?
                if newY >= COLOR_BOX_Y and newY <= COLOR_BOX_Y + COLOR_BOX_HEIGHT: 
                
                    #if clicked blue box 
                    if newX >= BLUEBOX_X and newX<= BLUEBOX_X + COLOR_BOX_WIDTH: 
                        color_click = "blue" 
                        
                    #if clicked cycle box 
                    if newX >= CYCLEBOX_X and newX <= CYCLEBOX_X + COLOR_BOX_WIDTH: 
                        color_click = "cycle"
                        
                    #if clicked segment box 
                    if newX >= SEGBOX_X and newX <= SEGBOX_X + COLOR_BOX_WIDTH: 
                        color_click = "segment" 
                    
            
                #if click on segment bar, slider is turned on 
                if newX >= SEGMENT_CLICK_MIN and newX <= SEGMENT_CLICK_MAX and newY >= 525 and newY <= 550: 
                    segment_slide = True
                    
        
                #likewise for the angle slider 
                if newX >= ANGLE_CLICK_MIN and newX <= ANGLE_CLICK_MAX and newY >= 525 and newY <= 550: 
                    angle_slide = True 
                    
            
            #if let go of mouse, draggers go back to being false         
            elif Draw.mouseRelease():  
                angle_slide = False 
                segment_slide = False 
                             
        #if user is holding down mouse on segment bar        
        if segment_slide: 
            if Draw.mouseMoved():
            #variables to store where the mouse is 
                newX, newY = Draw.currentMouse() 
            
            #if its in the range of the slider bar then reassign segment_knob 
            #to where the mouse is. makes more wiggleroom for y value 
                if newX >= SEGMENT_CLICK_MIN and newX<= SEGMENT_CLICK_MAX and newY >= 475 and newY <= 575: 
                    segment_knob = newX 
        
        #if user is holding down mouse on angle bar         
        if angle_slide: 
            if Draw.mouseMoved():
            #variables to store where the mouse is 
                newX, newY = Draw.currentMouse() 
            
            #if its in the range of angle bar then reassign angle_knob to 
            #where the mouse is. makes more wiggleroom for y value 
                if newX >= ANGLE_CLICK_MIN and newX<= ANGLE_CLICK_MAX and newY >= 475 and newY <= 575: 
                    angle_knob = newX
        
        #call for spiro to be displayed on the screen!              
        drawBoard(segment_knob, angle_knob, color_click) 
        
    
def main(): 
    Draw.setCanvasSize(CANVAS_WIDTH, CANVAS_HEIGHT)
    user()
      
main()    
