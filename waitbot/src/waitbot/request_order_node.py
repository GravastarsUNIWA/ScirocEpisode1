#!/usr/bin/python3

import os
import sys
from time import sleep
import json

import rospy
from std_msgs.msg import String


class req_order():
    def __init__(self):
        # TODO put all correct items
        self.items = ['cocacola',
                      'sprite',
                      'fanta']
        # ,
        # 'estathe',
        # 'beer',
        # 'pringles1',
        # 'pringles2',
        # 'bifrutas_tropical_can',
        # 'biscuits_pack',
        # 'cup_glass_new',
        # 'cup_paper',
        # 'peroni',
        # 'plastic_cup',
        # 'tea_box'
        # ]

        self.banner = """
        =================================================
        
         _       __      _ __  __          __ 
        | |     / /___ _(_) /_/ /_  ____  / /_
        | | /| / / __ `/ / __/ __ \/ __ \/ __/
        | |/ |/ / /_/ / / /_/ /_/ / /_/ / /_  
        |__/|__/\__,_/_/\__/_.___/\____/\__/  
                                    
        =================================================
        """

        self.welcome_msg = 'Hello, I am a Waitbot.\nWhat would you like to order?'

        # rospy.init_node('request_order_node')
        self.order_pub = rospy.Publisher(
            '/waitbot/orderList', String, queue_size=5)

    def typewriter(self, msg):
        for char in msg:
            sleep(0.1)
            sys.stdout.write(char)
            sys.stdout.flush()

    def print_items(self, items):
        msg = items[0]
        for i in range(1, len(items)):
            print (msg+"\r")
            sleep(0.3)
            msg += ' ' + items[i]
        print('')

    def wrong_order(self):
        print('\n')

        order = []

        while len(order) < 3:
            order_str = raw_input('Order item: ').strip().lower()
            if rospy.is_shutdown():
                return False

            if order_str not in self.items:
                print(order_str + ' is not available. Please order something else')
            else:
                order.append(order_str)
                print('current order: ' + ', '.join(order))

        if rospy.is_shutdown():
            return False

        print('\nYou ordered: ' + ', '.join(order))
        valid = raw_input(
            'If your order is correct press OK or press anything to order again:\n')
        if valid == 'OK':
            self.order_pub.publish(json.dumps(order))
            return True
        else:
            print('Please order again')
            return "loop"

    def order(self):
        print('\n')
        print(self.banner)

        self.typewriter(self.welcome_msg)
        print('\n')

        print('CATALOG')
        self.print_items(self.items)

        order = []

        while len(order) < 3:
            order_str = raw_input('Order item: ')  # .strip().lower()
            if rospy.is_shutdown():
                return False

            if order_str not in self.items:
                print(order_str + ' is not available. Please order something else')
            else:
                order.append(order_str)
                print('current order: ' + ', '.join(order))

        if rospy.is_shutdown():
            return False

        print('\nYou ordered: ' + ', '.join(order))
        valid = raw_input(
            'If your order is correct press OK or press anything to order again:\n')
        if valid == 'OK':
            self.order_pub.publish(json.dumps(order))
            return True
        else:
            print('Please order again')
            return "loop"

    def main(self):
        answer = self.order()

        while True:
            try:
                if answer is 'loop':
                    pass
                elif answer is False or answer is True:
                    return True

            except rospy.ROSInterruptException:
                rospy.loginfo("Order is disrupted")

            answer = self.wrong_order()


if __name__ == '__main__':
    main = req_order()
