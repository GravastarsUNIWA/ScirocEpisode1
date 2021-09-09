#!/usr/bin/env python

import os
import rospy
import json
import smach
import collections
from std_msgs.msg import String


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

class ConfirmOrder(smach.State):

    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['correct', 'false'])
        self.msg = msg

        self.order_sub = rospy.Subscriber("/waitbot/table_manager/orderList", String, self.order_callback)
        self.counter_sub = rospy.Subscriber("counter_items", string_array, self.counter_callback)

    def order_callback(self, msg):
        self.items_on_order = json.loads(msg.data)
    def counter_callback(self, msg):
        self.items_on_paso = msg.data

    def execute(self, userdata):
        # msg = rospy.wait_for_message(topic, topicType, timeout) (edited) 
        # 
        if collections.Counter(self.items_on_order) == collections.Counter(self.items_on_paso):
            return 'correct'
        else:
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
        # Create publisher tabletoorder

    def execute(self, userdata):

        # move to tabletoorder and call service
        os.system('rosservice call /sciroc_object_manager/move_items_on_the_closest_table')
        return 'done'
