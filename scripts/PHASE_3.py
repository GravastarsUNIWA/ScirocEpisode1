#!/usr/bin/env python

import os
import rospy
import smach
import collections
from uniwa_nav_stack.msg import string_array


class Wait(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done','skip'])
        self.msg = msg

    def execute(self, userdata):
        print self.msg + ":"
        result = raw_input()
        if result.lower() == 's' or result.lower() == 'skip':
            return 'skip'
        else:
            return 'done'


class SpawnOrder(smach.State):
    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

        self.order_sub = rospy.Subscriber("order_publisher", string_array, self.order_callback)

    def order_callback(self, msg):

        self.item1 = msg.data[0]
        self.item2 = msg.data[1]
        self.item3 = msg.data[2]

    def execute(self, userdata):
        #
        os.system('rosservice call /sciroc_object_manager/get_three_ordered_items %s %s %s' % (self.item1, self.item2, self.item3))
        return 'done'

class ConfirmOrder(smach.State):

    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['correct', 'false'])
        self.msg = msg

        self.order_sub = rospy.Subscriber("order_publisher", string_array, self.order_callback)
        self.counter_sub = rospy.Subscriber("counter_items", string_array, self.counter_callback)

    def order_callback(self, msg):
        self.items_on_order = msg.data
    def counter_callback(self, msg):
        self.items_on_paso = msg.data

    def execute(self, userdata):
        if collections.Counter(self.items_on_order) == collections.Counter(self.items_on_paso):
            return 'correct'
        else:
            return 'false'

class CorrectOrder(smach.State):

    def __init__(self, msg):
        smach.State.__init__(self, outcomes=['done'])
        self.msg = msg

        self.order_sub = rospy.Subscriber("order_publisher", string_array, self.order_callback)
        self.counter_sub = rospy.Subscriber("counter_items", string_array, self.counter_callback)

    def order_callback(self, msg):
        self.items_on_order = msg.data
    def counter_callback(self, msg):
        self.items_on_paso = msg.data


    def execute(self, userdata):
        wrong_item = collections.Counter(self.items_on_paso) - collections.Counter(self.items_on_order)
        wrong_item = wrong_item.keys()
        wrong_item_num = (collections.Counter(self.items_on_paso) - collections.Counter(self.items_on_order)).items()[0][1]

        correct_item = collections.Counter(self.items_on_order) - collections.Counter(self.items_on_paso)
        correct_item = correct_item.keys()
        correct_item_num = (collections.Counter(self.items_on_order) - collections.Counter(self.items_on_paso)).items()[0][1]

        print("I got wrong item(s)")
        print(wrong_item , wrong_item_num)

        print("I want the following item(s)")
        print(correct_item , correct_item_num)

        #os.system('rosservice call /sciroc_object_manager/change_the_item %s %s' % (wrong_item, correct_item))

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

