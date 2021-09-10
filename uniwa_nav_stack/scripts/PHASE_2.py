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
        self.get_name_of_table_order_pub = rospy.Publisher('/table_status/table_to_order',String, queue_size=1)

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
                self.get_name_of_table_order_pub.publish(tableName)

            # Publisher for nlp_parser
            self.table_ready_pub.publish(True)

        return 'done'

class GetSpeechOrder(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.all_table_status_sub = rospy.Subscriber('/table_status/all_table_status', String, self.serving_callback)
        self.all_table_status_pub = rospy.Publisher('/table_status/all_table_status', String, queue_size=1)
        self.order_pub = rospy.Publisher('/table_status/ready', Bool, queue_size=1)

    def serving_callback(self,msg):
        self.all_table_status = json.loads(msg.data)

    def execute(self, userdata):

        # Wakeup waitbot
        self.order_pub.publish(True)

        order_list = rospy.wait_for_message('/waitbot/orderList', String)
        # print("Ordered items", order_list, type(order_list))

        # Get table to serve from 
        temp = self.all_table_status
        for table in temp:
            if temp[table]['Status']=="Serving":
                tabletoOrder = str(table)

        temp[tabletoOrder]["Order"]=(order_list.data) 
        self.all_table_status_pub.publish(json.dumps(temp))

        return 'done'