#!/usr/bin/env python

import os
import rospy
import smach
import collections
import json
import time
import json

from std_msgs.msg import String
from std_msgs.msg import Bool
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionFeedback
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, PointStamped
from geometry_msgs.msg import Pose, Point, Quaternion

from PHASE_1 import Move

from coordinates import Coordinates

class GetServingTables(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])

        self.table_ready_pub = rospy.Publisher('/table_status/ready', Bool, queue_size=1)
        self.all_table_status_sub = rospy.Subscriber('/table_status/all_table_status', String, self.serving_callback)
        
        # self.table_status = json.dumps({
        #     "table1": {"Items":False, "NoP": 2, "Status":"Serving" , "Order":[]},
        #     "table2": {"Items":False, "NoP": 3, "Status":"Served" , "Order":[]}
        #     })

    def serving_callback(self, msg):
        encoded_all_table_status = msg.data
        self.all_table_status = json.loads(encoded_all_table_status)


    def execute(self, userdata):
        c = Coordinates()
        c.init_location()
        
        tabletoOrder = ''
        tableName = ''
        table_st = self.all_table_status
        for table in table_st:
            if table_st[table]['Status']=="Serving":
                tabletoOrder = str(table)

        if tabletoOrder:
            if tabletoOrder == "table1":
                table = c.table1
                tableName="table1"
            elif tabletoOrder == "table2":
                table = c.table2
                tableName="table2"
            elif tabletoOrder == "table3":
                table = c.table3
                tableName="table3"
            elif tabletoOrder == "table4":
                table = c.table4
                tableName="table4"
            elif tabletoOrder == "table5":
                table = c.table5
                tableName="table5"
            elif tabletoOrder == "table6":
                table = c.table6
                tableName="table6"


            if table and tableName:
                self.movetoOrder=smach.StateMachine(outcomes=['finished'])
                with self.movetoOrder:
                    smach.StateMachine.add('MOVETOTABLE',
                                            Move(table, tableName), 
                                            transitions={'done':'finished'})
                self.movetoOrder.execute()

            self.table_ready_pub.publish(True)

        return 'done'

class GetSpeechOrder(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.all_table_status_sub = rospy.Subscriber('/table_status/all_table_status', String, self.serving_callback)
        self.all_table_status_pub = rospy.Publisher('/table_status/all_table_status', String, queue_size=1)
        self.order_pub = rospy.Publisher('/table_status/ready', Bool, queue_size=1)

        # adi gia auto ftiakse sub kai callback kai apo8hkeuse str st table_status
        self.order_list = ["cocacola", "cocacola",'sprite']
        # self.order_list = []



    def order_list_callback(self, msg):
        self.order_list = msg.data

    def serving_callback(self,msg):
        self.table_status = msg.data

    def execute(self, userdata):

        # Anoikse to waitbot
        self.order_pub.publish(True)

        while self.order_list != True:
            self.order_is_done_sub = rospy.Subscriber('/waitbot/orderList', String, self.order_list_callback)
            
            if len(self.order_list) >= 1:
                break

        # Get table to serve from 
        temp = json.loads(self.table_status)
        for table in temp:
            if temp[table]['Status']=="Serving":
                tabletoOrder = str(table)

        temp[tabletoOrder]["Order"]=(self.order_list) 
        self.all_table_status_pub.publish(json.dumps(temp))

        return 'done'



# class GetSpeechOrder(smach.State):
#     def __init__(self, msg):
#         smach.State.__init__(self, outcomes=['done'])

#     def execute(self, userdata):
#         # self.nlp = NLP()

#         os.system('roslaunch waitbot waitbot.launch')

#         return 'done'

