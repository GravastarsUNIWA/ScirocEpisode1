#!/usr/bin/env python

import math
import rospy
import roslaunch
import rospkg
import os
import sys
import tf
import numpy as np
import random

from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose, Point, Quaternion
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from sciroc_ep1_object_manager.srv import *
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import GetModelProperties
from gazebo_msgs.srv import GetJointProperties
from gazebo_msgs.srv import SpawnModel, DeleteModel


VERBOSE = False

object_counter = 0

ROBOT_TRAY_HEIGHT = 1.5     # height to move objects on the robot's tray                    
TABLE_CAFFE_HEIGHT = 1.1    # height to move objects on the table            
COUNTER_H = 1.3             # counter height        
COUNTER_POSE = np.array([4.5, -1.4, COUNTER_H])
MIN_DIST_TO_MOVE_OBJS = 1.5 # min distance to active the moving services [m]
OFFSET = 0.3                # distance of objects from the center of the table [m]
OFFSET_TRAY = 0.11          # distance of the tray from the center of the robot [m] 
OFFSET_OBJS_TRAY = 0.05
RANDOMIZE_SPAWN = True
CHECK_DISTANCES = False

SPAWN_POSES = (     #tuple
    Pose(position=Point(x=4.5, y=-1.4+OFFSET, z=COUNTER_H)),
    Pose(position=Point(x=4.5, y=-1.4, z=COUNTER_H)),
    Pose(position=Point(x=4.5, y=-1.4-OFFSET, z=COUNTER_H))
)

list_of_tables = {   #set
    "cafe_table", 
    "cafe_table_0", 
    "cafe_table_1", 
    "cafe_table_2", 
    "cafe_table_5",
    "cafe_table_6"
}

available_objects = {   #set
    "beer",
    "bifrutas_tropical_can",
    "biscuits_pack",
    #"coke_can",
    "cocacola",    
    "plastic_cup",
    "pringles1",
    "pringles2",
    "sprite",
}

objects_on_robot_tray = [  #list
    "none",
    "none",
    "none"
]

counter_object = "table"			

class sciroc_ep1_object_manager:
    def __init__(self):
        print("init")
        #self.cw_left = np.array([None, None, None, None])
		#				   self.ccw_right_callback, queue_size=1)   
        self.robot_pose = [0.0,0.0]		



def talker(se1om): #ONLY FOR TESTING PURPOSES
    if VERBOSE:
        print ("TALKER")

    r = rospy.Rate(10) #10hz
    msg = Float64()
#    load_and_spawn_gazebo_models("beer", 4.5, -2, 1.6)

    
    while not rospy.is_shutdown(): #ONLY FOR TESTING PURPOSES
        #msg = getDoorAperture()
        #ebws.door_pub.publish(msg)
        
        #load_and_spawn_gazebo_models("beer", 4.5, -2, 1.6)
        #spawn_three_objs("beer", "beer", "beer")
    #    move_items_on_the_tray()
    #    move_items_on_the_closest_table()
        
        r.sleep()


def callback(data):
    rospy.loginfo("%s is age: %d" % (data.name, data.age))
    print ("initialized")


def move_items_on_the_tray():   
    global OFFSET_OBJS_TRAY
    objs_on_robot_tray = get_objects_on_robot_tray()
    counter_distance = get_robot_counter_distance()
    #if counter_distance > MIN_DIST_TO_MOVE_OBJS:
    #    return 
 
    tray_pose = get_robot_tray_position()
#    self.objects_on_robot_tray #TODO check if needed to be put on global var 
    set_position(tray_pose[0]+OFFSET_OBJS_TRAY, 
                tray_pose[1]+OFFSET_OBJS_TRAY,
                tray_pose[2], 
                objs_on_robot_tray[0])

    set_position(tray_pose[0]+OFFSET_OBJS_TRAY, 
                tray_pose[1]-OFFSET_OBJS_TRAY,
                tray_pose[2], 
                objs_on_robot_tray[1])

    set_position(tray_pose[0]-OFFSET_OBJS_TRAY, 
                tray_pose[1]+OFFSET_OBJS_TRAY,
                tray_pose[2], 
                objs_on_robot_tray[2])



def move_items_on_the_tray_srv(req):  
    global CHECK_DISTANCES, MIN_DIST_TO_MOVE_OBJS
    
    if CHECK_DISTANCES:
        counter_distance = get_robot_counter_distance()
        if counter_distance > MIN_DIST_TO_MOVE_OBJS:
            return MoveItemsOnTheTrayResponse(False, "Robot too far from the counter to move items")
 
    move_items_on_the_tray()

    return MoveItemsOnTheTrayResponse(True, "Items moved")

def move_items_on_the_closest_table_srv(req):  
    global CHECK_DISTANCES, MIN_DIST_TO_MOVE_OBJS
    closest_table_position, table_distance = get_closest_table_position_and_distance()
    if CHECK_DISTANCES:
        if table_distance > MIN_DIST_TO_MOVE_OBJS:
            return MoveItemsOnClosestTableResponse(False, 
            "Robot too far from the table to move items")
    
    move_items_on_the_closest_table()
    print("move_objects_on_the_closest_table_srv service")
    return MoveItemsOnClosestTableResponse(True, "Items moved")

    
    
def move_items_on_the_closest_table():  
    objs_on_robot_tray = get_objects_on_robot_tray()
    closest_table_position, table_distance = get_closest_table_position_and_distance()    
    set_position(closest_table_position[0] - OFFSET, 
                closest_table_position[1] + OFFSET,
                TABLE_CAFFE_HEIGHT, 
                objs_on_robot_tray[0])

    set_position(closest_table_position[0] + OFFSET, 
                closest_table_position[1] - OFFSET,
                TABLE_CAFFE_HEIGHT, 
                objs_on_robot_tray[1])

    set_position(closest_table_position[0] + OFFSET, 
                closest_table_position[1] + OFFSET,
                TABLE_CAFFE_HEIGHT, 
                objs_on_robot_tray[2])

    
def get_three_ordered_items_srv(req):  
    available_objs = get_available_objects()

    if req.item0 not in available_objs:
        return GetThreeOrderedItemsResponse(False, 
        "First requested object is not valid object")        

    if req.item1 not in available_objs:
        return GetThreeOrderedItemsResponse(False, 
        "Second requested object is not valid object")    
        
    if req.item2 not in available_objs:
        return GetThreeOrderedItemsResponse(False, 
        "Third requested object is not valid object")    
    
    spawn_three_objs(req.item0, req.item1, req.item2)
    
    print("get_three_objects_srv service")
    return GetThreeOrderedItemsResponse(True, "") 

    
def spawn_three_objs(obj0, obj1, obj2) :
    global TABLE_BANK_POSE, OFFSET, RANDOMIZE_SPAWN, objects_on_robot_tray
    available_objs = get_available_objects()
    
    if RANDOMIZE_SPAWN:
        chosen = random.sample(available_objs, 1)[0]
        print(chosen)
        while chosen != obj0 and chosen != obj1 and chosen != obj2:
            chosen = random.sample(available_objs, 1)[0]
        objs = [obj0, obj1, obj2]
        print(objs)
        random_index = random.randrange(len(objs))
        objs[random_index] = chosen
        print(objs)
        obj0, obj1, obj2 = objs
    
    modlist, model0 = load_and_spawn_gazebo_models(obj0, SPAWN_POSES[0])   
    modlist, model1 = load_and_spawn_gazebo_models(obj1, SPAWN_POSES[1])   
    modlist, model2 = load_and_spawn_gazebo_models(obj2, SPAWN_POSES[2])   
    objects_on_robot_tray = [model0, model1, model2]
    print (objects_on_robot_tray)
    
    
def change_the_item_srv(req):  
    objs_on_tray = get_objects_on_robot_tray()
    available_objs = get_available_objects()
    
#    if not is_on_the_curr_ordered_objs(req.name_of_the_object_to_spawn):
#        return ChangeTheItemResponse(False, 
#        "Requested object is not on the counter")    
    
    if req.name_of_the_object_to_spawn not in available_objs:
        return ChangeTheItemResponse(False, 
        "Requested object is not valid object")    
        
    old_model_id = get_model_tray_id(req.name_of_the_object_to_change)
    if old_model_id == None:
        return ChangeTheItemResponse(False, 
        "Requestd object is not on the counter")    

    delete_model(old_model_id)
    print (old_model_id)
    print (objs_on_tray)
    position_of_old_item = objs_on_tray.index(old_model_id)
    modlist, new_model = load_and_spawn_gazebo_models(req.name_of_the_object_to_spawn,
     SPAWN_POSES[position_of_old_item])   
    
    if change_object_on_robot_tray_list(old_model_id, new_model):
        return ChangeTheItemResponse(True, "")
    return False
  
  
def delete_model(modelName):
    """ Remove the model with 'modelName' from the Gazebo scene """
    del_model_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel) # Handle to model spawner
    rospy.wait_for_service('gazebo/delete_model') # Wait for the model loader to be ready 
    del_model_prox(modelName) # Remove from Gazebo
  
def spawn_sdf(name, description_xml, pose, reference_frame):
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_sdf = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp_sdf = spawn_sdf(name, description_xml, "/", pose, reference_frame)
    except rospy.ServiceException as e:
        rospy.logerr("Spawn SDF service call failed: {0}".format(e)) 
  
def spawn_sdf_model(name, path, pose, reference_frame) :
    # Load Model SDF
    description_xml = ''
    with open(path, "r") as model_file:
        description_xml = model_file.read().replace('\n', '')
        spawn_sdf(name, description_xml, pose,reference_frame)
        
def load_and_spawn_gazebo_models(obj_name, pose):   
    model_list = []
    world_reference_frame = "world"
    # sorting_demo model path  
    ep1_models_path = rospkg.RosPack().get_path('sciroc_ep1_object_manager') + "/models/" 
    # Spawn object
    object_name = obj_name
    object_path = ep1_models_path + "/" + object_name+ "/model.sdf"
    #object_pose = Pose(position=Point(x=x_obj, y=y_obj, z=z_obj))
    object_pose = pose
    global object_counter 
    spawn_sdf_model(object_name+str(object_counter), 
        object_path, 
        object_pose, 
        world_reference_frame)
    current_model = object_name+str(object_counter)
    model_list.append(current_model)
    object_counter+= 1
    return model_list, current_model
    
def is_there_an_object_on(x,y,z):
    return False

def get_available_objects() :
    global available_objects
    return available_objects

def get_objects_on_robot_tray() :
    global objects_on_robot_tray
    return objects_on_robot_tray

def set_objects_on_robot_tray(model0, model1, model2) :  
    global objects_on_robot_tray
    objects_on_robot_tray = (model0, model1, model2)
    
def change_object_on_robot_tray_list(old, new) :  
    global objects_on_robot_tray
    for n, curr_item_with_id in enumerate(objects_on_robot_tray):
        if old in curr_item_with_id: 
            objects_on_robot_tray[n] = new
            return True
    return False

def is_on_the_curr_ordered_objs(obj) :  
    global objects_on_robot_tray
    for n, curr_item_with_id in enumerate(objects_on_robot_tray):
        if obj in curr_item_with_id: 
            return True
    return False

def get_model_tray_id(obj):
    global objects_on_robot_tray
    for n, curr_item_with_id in enumerate(objects_on_robot_tray):
        if obj in curr_item_with_id: 
            return curr_item_with_id
    return None
    
def set_position(goal_x, goal_y, goal_z, object_to_move):
    state_msg = ModelState()

    state_msg.model_name = object_to_move
    state_msg.pose.position.x = goal_x
    state_msg.pose.position.y = goal_y
    state_msg.pose.position.z = goal_z
    state_msg.pose.orientation.x = 1
    state_msg.pose.orientation.y = 0
    state_msg.pose.orientation.z = 0
    state_msg.pose.orientation.w = 0

    rospy.wait_for_service('/gazebo/set_model_state')
    try:
       set_state = rospy.ServiceProxy(
          '/gazebo/set_model_state', SetModelState)
       resp = set_state(state_msg)
       #print(state_msg)

    except rospy.ServiceException, e:
       print "Service call failed: %s" % e

def get_robot_position() :           #OK
    try:
        model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        resp_coordinates = model_coordinates('tiago', '')
    except rospy.ServiceException, e:
        print "ServiceProxy failed: %s"%e
        exit(0)
    if VERBOSE:
        print 'Status.success = ', resp_coordinates.success
        print("robot pose " + str(resp_coordinates.pose.position.x))
        print("robot pose " + str(resp_coordinates.pose.position.y))
    return np.array([resp_coordinates.pose.position.x, resp_coordinates.pose.position.y])
    
def get_robot_orientation() :        #OK
    try:
        model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        resp_coordinates = model_coordinates('tiago', '')
    except rospy.ServiceException, e:
        print "ServiceProxy failed: %s"%e
        exit(0)
    quaternion = (
        resp_coordinates.pose.orientation.x,
        resp_coordinates.pose.orientation.y,
        resp_coordinates.pose.orientation.z,
        resp_coordinates.pose.orientation.w)
    euler = tf.transformations.euler_from_quaternion(quaternion)
    roll = euler[0]
    pitch = euler[1]
    yaw = euler[2]
    if VERBOSE:
        print 'Status.success = ', resp_coordinates.success
        print("robot orientation " + str(yaw))
    return yaw
    
def get_robot_tray_position():          
    robot_pose = get_robot_position()
    robot_orientation = get_robot_orientation()
    print ("robot orientation")
    print (robot_orientation)
    return np.array(
        [robot_pose[0] - OFFSET_TRAY*math.cos(robot_orientation), 
        robot_pose[1] - OFFSET_TRAY*math.sin(robot_orientation),
        ROBOT_TRAY_HEIGHT]
    )
    


def get_closest_table_position_and_distance(): #OK
    global list_of_tables
    min_distance = 1000000
    closest_table_position = np.array([0,0])
    for table in list_of_tables:
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            resp_coordinates = model_coordinates(table, '')
            curr_table_coords = np.array([
                resp_coordinates.pose.position.x,
                resp_coordinates.pose.position.y])
            curr_min_dist = np.linalg.norm(get_robot_position() - curr_table_coords)
            if curr_min_dist  < min_distance:
                closest_table_position = curr_table_coords
                min_distance = curr_min_dist
        except rospy.ServiceException, e:
            print "ServiceProxy failed: %s"%e
            #exit(0)
    
    return closest_table_position, min_distance


def get_robot_counter_distance(): #OK
    global counter_object
    try:
        model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        resp_coordinates = model_coordinates(counter_object, '')
        counter_coords = np.array([
            resp_coordinates.pose.position.x,
            resp_coordinates.pose.position.y])
        dist = np.linalg.norm(get_robot_position() - counter_coords)
    except rospy.ServiceException, e:
        print "ServiceProxy failed: %s"%e
        #exit(0)
    return dist



def listener(self):
    image_camera = rospy.Subscriber("sensor_msgs/Image", Image, callback)


def main(args):
     se1om =  sciroc_ep1_object_manager()
     rospy.init_node('sciroc_ep1_object_manager', anonymous=True) 
     
     listener(se1om)

     s = rospy.Service('/sciroc_object_manager/move_items_on_the_tray', 
     MoveItemsOnTheTray, move_items_on_the_tray_srv) 
     s = rospy.Service('/sciroc_object_manager/move_items_on_the_closest_table', 
     MoveItemsOnClosestTable, move_items_on_the_closest_table_srv) 
     s = rospy.Service('/sciroc_object_manager/get_three_ordered_items', 
     GetThreeOrderedItems, get_three_ordered_items_srv) 
     s = rospy.Service('/sciroc_object_manager/change_the_item', 
     ChangeTheItem, change_the_item_srv) 
     

     try:
         talker(se1om)
         rospy.spin()
     except KeyboardInterrupt:
           print ("Shutting down sciroc_ep1_object_manager module")



if __name__ == '__main__':
     main(sys.argv)
