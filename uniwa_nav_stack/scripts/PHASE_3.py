#!/usr/bin/env python

import os
import rospy
import json
import smach
import collections
from std_msgs.msg import String
import roslaunch
from coordinates import Coordinates
from PHASE_1 import Move

class Wait(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        # print('sleeping')
        rospy.sleep(0.5)
        return 'done'

class SpawnOrder(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.get_name_of_table_order_sub = rospy.Subscriber("/table_status/table_to_order",String, self.get_name_of_table_order_callback)
        self.order_sub = rospy.Subscriber("/table_status/all_table_status", String, self.all_table_status_callback)
        self.order_table_name = None


    def get_name_of_table_order_callback(self,msg):
        self.order_table_name = msg.data

    def all_table_status_callback(self, msg):
        if self.order_table_name:
            encoded_items = msg.data
            decoded_items = json.loads(encoded_items)
            items = json.loads(decoded_items[self.order_table_name]['Order'])

            self.item1 = str(items[0])
            self.item2 = str(items[1])
            self.item3 = str(items[2])

    def execute(self, userdata):

        os.system('rosservice call /sciroc_object_manager/get_three_ordered_items %s %s %s' % (self.item1, self.item2, self.item3))
        return 'done'

class SpawnYolo(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        os.system("rosnode kill /yolov5_object_detector")

        #docker path
        # w_path = "/home/user/ws/src/ScirocEpisode1/ros_yolov5/weights/plus_ultra.pt"

        # native path
        # w_path = "/home/paris/tiago_public_ws/src/ros_yolov5/weights/plus_ultra.pt"

        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        cli_args = ['ros_yolov5', 'ros_yolov5_2.launch', 'weights_path:=/home/paris/tiago_public_ws/src/ros_yolov5/weights/plus_ultra.pt']
        roslaunch_args = cli_args[1:]
        roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]


        rospy.loginfo("YOLO PLUS ULTRA started")
        launch = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
        launch.start()
        return 'done'

class ConfirmOrder(smach.State):

    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['correct', 'false'])
        self.msg = msg
        self.order_table_name = None
        self.get_name_of_table_order_sub = rospy.Subscriber("/table_status/table_to_order",String, self.get_name_of_table_order_callback)
        self.order_sub = rospy.Subscriber("/table_status/all_table_status", String, self.order_callback)


    def get_name_of_table_order_callback(self,msg):
        self.order_table_name = msg.data


    def order_callback(self, msg):
        if self.order_table_name:
            encoded_items = msg.data
            decoded_items = json.loads(encoded_items)
            self.items_on_order = str(decoded_items[self.order_table_name]['Order'])
            print("PEOS ",self.items_on_order, type(self.items_on_order))


    def execute(self, userdata):
        topic = '/object_detection/objects'
        msg = rospy.wait_for_message(topic, String)
        # print(msg, type(msg))
        items_on_paso = json.loads(msg.data)
        print("peos2 ",items_on_paso, type(items_on_paso))


        if len(items_on_paso) >=2:
            items_on_paso = [items_on_paso[0][-1], items_on_paso()[1][-1], items_on_paso()[2][-1]]


        if len(items_on_paso<2):
            return 'correct'

        
        # print(items_on_paso, type(items_on_paso))

        if collections.Counter(self.items_on_order) == collections.Counter(items_on_paso):
            # print(self.items_on_order, items_on_paso)
            # print(type(self.items_on_order), type(items_on_paso))
            print("CORRECT")
            return 'correct'
        else:
            # print(self.items_on_order, items_on_paso)
            # print(type(self.items_on_order), type(items_on_paso))
            print("FALSE")
            return 'false'

class CorrectOrder(smach.State):

    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.order_sub = rospy.Subscriber("/waitbot/orderList", String, self.order_callback)


    def order_callback(self, msg):
        self.items_on_order = json.loads(msg.data)


    def execute(self, userdata):
        topic = '/object_detection/objects'
        msg = rospy.wait_for_message(topic, String)
        itms = json.loads(msg.data)
        items_on_paso = [itms[0][-1], itms()[1][-1], itms()[2][-1]]

        self.wrong_item = collections.Counter(items_on_paso) - collections.Counter(self.items_on_order)
        self.wrong_item = self.wrong_item.keys()
        self.wrong_item_num = (collections.Counter(items_on_paso) - collections.Counter(self.items_on_order)).items()[0][1]
        self.correct_item = collections.Counter(self.items_on_order) - collections.Counter(items_on_paso)
        self.correct_item = self.correct_item.keys()
        self.correct_item_num = (collections.Counter(self.items_on_order) - collections.Counter(items_on_paso)).items()[0][1]
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
        self.all_table_status_sub = rospy.Subscriber('/table_status/all_table_status', String, self.serving_callback)
        self.all_table_status_pub = rospy.Publisher('/table_status/all_table_status', String, queue_size=1)
        self.get_name_of_table_order_sub = rospy.Subscriber("/table_status/table_to_order",String, self.get_name_of_table_order_callback)

    def serving_callback(self, msg):
        self.all_table_status = json.loads(msg.data)
        
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

        self.all_table_status[tableName]['Status'] = "Served"
        self.all_table_status_pub.publish(json.dumps(self.all_table_status))

        return 'done'

class ServeItems(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['more', 'fin'])
        self.msg = msg

        self.all_table_status_sub = rospy.Subscriber('/table_status/all_table_status', String, self.serving_callback)


    def serving_callback(self, msg):
        self.encoded_all_table_status = msg.data
        self.decoded_all_table_status = json.loads(self.encoded_all_table_status)
        self.all_table_status = self.decoded_all_table_status

    def execute(self, userdata):

        os.system('rosservice call /sciroc_object_manager/move_items_on_the_closest_table')

        table_st = self.all_table_status
        pt_counter = 0
        for table in table_st:
            if table_st[table]['Status'] == "Serving":
                pt_counter += 1 

        if pt_counter:
            return 'more'

        return 'fin'