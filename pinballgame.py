import math
import matplotlib.pyplot as mp 
from matplotlib.collections import EventCollection
import copy 

#define the pinballs initial location as the origin 



'''function to determine if we are colloding with the line.  Returns true if we hit the line, else returns false '''

def line_collision(LP1,LP2,pinball_cords):
    
    #equation of the line is just y = 2 
    if pinball_cords[1] >= 2:
        return True  #the pinball hits the line
    else:
        return False #the pinball does not hit the line 


''' fucntion to determine if we are colliding with the circle. Returns true if we do, otherwise returns false'''

def circle_collision(circle_center,circle_radius,pinball_cords):
    
    if round((pinball_cords[0] - 2)**2 + pinball_cords[1]**2,1) <= 1:
        return True  #the pinball hits the circle 
    else:
        return False #the pinball does not hit the circle 

'''function to take in the inital cords of the pinball, as well as the launch cords and the step length. then return the new cords'''
def move_pinball(pinball_cords, launch_angle_degrees, step):
    #step is acting as the hypotenuse of the triangle.  basically how far do we want to move in each "step" of the cycle. 
    #the smaller the step the more accurate the trajectory 
    adjacent_side = math.cos(math.radians(launch_angle_degrees)) * step  #converts the degrees to radians 
    opposite_side = math.sqrt(step**2-adjacent_side**2)
    pinball_cords[1] += adjacent_side 
    pinball_cords[0] += opposite_side * (launch_angle_degrees/abs(launch_angle_degrees))
    pinball_cords[0] = pinball_cords[0]
    pinball_cords[1] = pinball_cords[1]
    return pinball_cords

'''function that handles the angle of reflection upon hitting the line.  the angle of incidence should be the same as the angle 
of reflection, but we want the direction to change, so we can use the supplement of the angle of incident '''

def line_collision_redirection(launch_angle_degrees):
    if launch_angle_degrees>0 :
        return 180-launch_angle_degrees
    else: 
        return -(180-launch_angle_degrees)
'''function that determines the angle of collision with the circle. we should be able to determine the tangent line to the point
of collision, and going from there we should be able to tell what the angle of reflection is to be (the same as the incidence angle) 
return the new pinball coords and current launch angle in degree'''

def ciricle_collision_redirection(launch_angle_degrees, angle_of_tangent):
    angle_of_reflection = 180-launch_angle_degrees
    angle_of_reflection -= angle_of_tangent
    if launch_angle_degrees > 0:
        return angle_of_reflection  
    else: 
        return -angle_of_reflection
'''inbound angle is 150 degrees, so AOR is 30 degrees. if it hits a 30 degree
tangent line, its AOR should be 0.  '''
'''inbound angle is 150 degrees, so AOR is 30 degrees. if it hits a -45degree
tangent line, its AOR should be 195.  '''
'''inbound angle is 150 degrees, so AOR is 30 degrees. if it hits a -30degree
tangent line, its AOR should be 180.  '''


'''function to determine the tangent line to the point at the circle we have collided with
this is where its going to get tricky beause the tangent line will not be parallel to the upper line.  So we are going to need to refactor 
the coordinate system to accomodate the new "flat"  IE.  if the tangent is at a 45 deg slope to the original line, a 45 degree incidence 
angle would lead to a 90 degree angle of reflection with respect to the initial line.  
'''

def tangent_determinant(circle_center, circle_radius, collision_point):
    slope_of_radius = (collision_point[1]-circle_center[1])/ ( collision_point[0]-circle_center[0])
    slope_of_tangent = -1/slope_of_radius #negative reciproical of the slope of the radius 
    slope_of_tangent_degrees = math.degrees(math.atan(slope_of_tangent)) #take the gradient and turn it into degrees
    #need to determine the angle of the tangent line from our "baseline" or flat 
    #print(slope_of_tangent_degrees)
    return slope_of_tangent_degrees


#test of the movement
'''function to test the angle of interst and spit out a list with the angle and the maximum 
number of collisions that we get from that answer'''

def simulator(current_launch_angle,maximum):
    pinball = [0,0]
    circle_center = [2,0]
    circle_radius = 1
    line_point_1 = [2,0]
    line_point_2 = [2,10]
    path_of_travel = []

    #make a deep cope of the current launch angle that will act as the inital 
    initial_launch_angle = copy.deepcopy(current_launch_angle)
    
    bounces = 0
    while pinball[0]<3.5 and pinball[0] > -3.5 and pinball[1]<3.5 and pinball[1] > -.5:
   
        pinball = move_pinball(pinball,current_launch_angle,.008)
    
        path_of_travel.append(copy.deepcopy(pinball))
        if line_collision(line_point_1,line_point_2,pinball):
            current_launch_angle = line_collision_redirection(current_launch_angle)
            bounces += 1 
           

            
        if circle_collision(circle_center,circle_radius, pinball):
            tangent_line = tangent_determinant(circle_center,circle_radius,pinball)
            bounces += 1
            current_launch_angle = ciricle_collision_redirection(current_launch_angle,tangent_line)
        
        
    if maximum == True:
        
        #seperate the logged coordinates into x and y positions     
        x_cords= []
        y_cords = []

        x_cords_line=[0,1,2,3,]
        y_cords_line=[2,2,2,2,]

        x_cords_circle=[2,1,3,2]
        y_cords_circle=[1,0,0,-1]

        for cord in path_of_travel:
            x_cords.append(cord[0])
            y_cords.append(cord[1])

        fig = mp.figure()
        ax1 = fig.add_subplot()

        ax1.scatter(x_cords,y_cords)
        ax1.scatter(x_cords_line,y_cords_line)
        ax1.scatter(x_cords_circle,y_cords_circle)

        mp.show()

    return [initial_launch_angle, bounces]
answers = []

for i in range(28223929770,28223929790):
    answers.append(simulator((i/1000000000),False))

print(answers)

simulator(28.2239298,True)

''' 45 and 45 should give 90, 45 and -45 should give 180

'''
