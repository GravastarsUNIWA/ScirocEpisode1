#!/usr/bin/env python

import os
import rospy
import json
import smach
import collections
from std_msgs.msg import String
import roslaunch
from coordinates import Coordinates


class Wait(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        # print('sleeping')
        rospy.sleep(0.1)
        return 'done'

class SpawnOrder(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.get_name_of_table_order_sub = rospy.Subscriber("/table_status/table_to_order",String, self.get_name_of_table_order_callback)

        self.order_sub = rospy.Subscriber("/table_status/all_table_status", String, self.order_callback)

        self.item1 = 'sprite'
        self.item2 = "cocacola"
        self.item3 = "cocacola"
        rospy.sleep(1)        

    def get_name_of_table_order_callback(self,msg):
        self.order_table_name = msg.data

    def order_callback(self, msg):

        encoded_items = msg.data
        decoded_items = json.loads(encoded_items)
        self.items = decoded_items[self.order_table_name]['Order']

        self.item1 = str(self.items[0])
        self.item2 = str(self.items[1])
        self.item3 = str(self.items[2])



    def execute(self, userdata):

        os.system('rosservice call /sciroc_object_manager/get_three_ordered_items %s %s %s' % (self.item1, self.item2, self.item3))
        return 'done'

class SpawnYolo(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg


    
    def execute(self, userdata):
        os.system("rosnode kill /yolov5_object_detector")
        rospy.sleep(1)

        #docker path
        # w_path = "/home/user/ws/src/ScirocEpisode1/ros_yolov5/weights/counter_weights.pt"

        # native path
        w_path = "/home/paris/tiago_public_ws/src/ros_yolov5/weights/counter_weights.pt"

        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        cli_args = ['ros_yolov5', 'ros_yolov5_2.launch', 'weights_path:=/home/paris/tiago_public_ws/src/ros_yolov5/weights/counter_weights.pt']
        roslaunch_args = cli_args[1:]
        roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]


        rospy.loginfo("YOLO 2 started")
        launch = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
        launch.start()
        return 'done'

class ConfirmOrder(smach.State):

    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['correct', 'false'])
        self.msg = msg
        self.get_name_of_table_order_sub = rospy.Subscriber("/table_status/table_to_order",String, self.get_name_of_table_order_callback)
        self.order_sub = rospy.Subscriber("/table_status/all_table_status", String, self.order_callback)
        
        self.items_on_order = ['sprite','cocacola','cocacola']
        rospy.sleep(1) 
        # self.yolo_sub = rospy.Subscriber('',String, self.order_callback)


    def get_name_of_table_order_callback(self,msg):
        self.order_table_name = msg.data


    def order_callback(self, msg):

        encoded_items = msg.data
        decoded_items = json.loads(encoded_items)
        self.items_on_order = decoded_items[self.order_table_name]['Order']


    def execute(self, userdata):
        topic = '/object_detection/counter'
        msg = rospy.wait_for_message(topic, String)
        print(msg, type(msg))

        # msg = rospy.wait_for_message(topic, topicType, timeout) (edited) 
        # 

        if collections.Counter(self.items_on_order) == collections.Counter(self.items_on_paso):
            print(self.items_on_order, self.items_on_paso)
            print(type(self.items_on_order), type(self.items_on_paso))
            return 'correct'
        else:
            print(self.items_on_order, self.items_on_paso)
            print(type(self.items_on_order), type(self.items_on_paso))
            return 'false'

class CorrectOrder(smach.State):

    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.order_sub = rospy.Subscriber("/waitbot/table_manager/orderList", String, self.order_callback)
        self.counter_sub = rospy.Subscriber("counter_items", string_array, self.counter_callback)

    def order_callback(self, msg):
        self.items_on_order = json.loads(msg.data)
    def counter_callback(self, msg):
        self.items_on_paso = msg.data

    def execute(self, userdata):
        self.wrong_item = collections.Counter(self.items_on_paso) - collections.Counter(self.items_on_order)
        self.wrong_item = self.wrong_item.keys()
        self.wrong_item_num = (collections.Counter(self.items_on_paso) - collections.Counter(self.items_on_order)).items()[0][1]
        self.correct_item = collections.Counter(self.items_on_order) - collections.Counter(self.items_on_paso)
        self.correct_item = self.correct_item.keys()
        self.correct_item_num = (collections.Counter(self.items_on_order) - collections.Counter(self.items_on_paso)).items()[0][1]
        os.system('rosservice call /sciroc_object_manager/change_the_item %s %s' % (self.wrong_item[0], self.correct_item[0]))
        return 'done'

class Pickuporder(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        os.system('rosservice call /sciroc_object_manager/move_items_on_the_tray')
        return 'done'

class Serve(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.get_name_of_table_order_sub = rospy.Subscriber("/table_status/table_to_order",String, self.get_name_of_table_order_callback)
        
        # Create publisher tabletoorder
    def get_name_of_table_order_callback(self,msg):
            self.order_table_name = msg.data

    def execute(self, userdata):
        c = Coordinates()
        c.init_location()
        if self.order_table_name == "table1":
                table = c.table1
                tableName="table1"
        elif self.order_table_name == "table2":
            table = c.table2
            tableName="table2"
        elif self.order_table_name == "table3":
            table = c.table3
            tableName="table3"
        elif self.order_table_name == "table4":
            table = c.table4
            tableName="table4"
        elif self.order_table_name == "table5":
            table = c.table5
            tableName="table5"
        elif self.order_table_name == "table6":
            table = c.table6
            tableName="table6"

        self.movetoOrder=smach.StateMachine(outcomes=['finished'])
        with self.movetoOrder:
            smach.StateMachine.add('MOVETOTABLE',
                                    Move(table, tableName), 
                                    transitions={'done':'finished'})
        self.movetoOrder.execute()

        # move to tabletoorder and call service
        return 'done'

class ServeItems(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        os.system('rosservice call /sciroc_object_manager/move_items_on_the_closest_table')
        return 'done'

