#!/usr/bin/env python
import os
import rospy
import json
import smach
import collections
from std_msgs.msg import String
import unicodedata

class Wait(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

    def execute(self, userdata):
        # print (self.msg + ":")
        rospy.sleep(2)
        return 'done'


class SpawnOrder(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.order_sub = rospy.Subscriber('/table_status/all_table_status', String, self.order_callback)
        # self.decoded_items = []
        rospy.sleep(2)


    def order_callback(self, msg):

        encoded_items = msg.data
        self.decoded_items = json.loads(encoded_items)

        # print(decoded_items)
        # self.item1 = str(json.loads(self.encoded_items)["table1"]["Order"][0])
        # self.item2 = str(json.loads(self.encoded_items)["table1"]["Order"][1])
        # self.item3 = str(json.loads(self.encoded_items)["table1"]["Order"][2])

    def execute(self, userdata):
        temp = self.decoded_items

        for table in temp:
            if temp[table]['Status']=="Serving":
                tabletoOrder = table

        print("KENOOOOOO",self.decoded_items)
        self.item1 = self.decoded_items[tabletoOrder]["Order"][0]
        self.item2 = self.decoded_items[tabletoOrder]["Order"][1]
        self.item3 = self.decoded_items[tabletoOrder]["Order"][2]


        os.system('rosservice call /sciroc_object_manager/get_three_ordered_items %s %s %s' % (self.item1, self.item2, self.item3))
        return 'done'

class ConfirmOrder(smach.State):

    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['correct', 'false'])
        self.msg = msg

        self.order_sub = rospy.Subscriber("/table_status/all_table_status", String, self.order_callback)
        self.counter_sub = rospy.Subscriber("/counter_items", String, self.counter_callback)

    def order_callback(self, msg):
        self.items_on_order = json.loads(msg.data)
    def counter_callback(self, msg):
        self.items_on_paso = json.loads(msg.data)
        #see if list

    def execute(self, userdata):
        if collections.Counter(self.items_on_order) == collections.Counter(self.items_on_paso):
            return 'correct'
        else:
            return 'false'

class CorrectOrder(smach.State):

    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg
        self.order_sub = rospy.Subscriber("/waitbot/table_manager/orderList", String, self.order_callback)
        self.counter_sub = rospy.Subscriber("/counter_items", String, self.counter_callback)

    def order_callback(self, msg):
        self.items_on_order = json.loads(msg.data)
    def counter_callback(self, msg):
        self.items_on_paso = json.loads(msg.data)
        print(self.items_on_paso)

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

    def execute(self, userdata):
        os.system('rosservice call /sciroc_object_manager/move_items_on_the_closest_table')
        return 'done'

