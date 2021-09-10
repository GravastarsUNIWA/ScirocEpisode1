#!/usr/bin/python3

import os
import sys
from time import sleep
import json

import rospy
from std_msgs.msg import String

items = ['cocacola',
         'sprite',
         'fanta',
         'estathe',
         'beer',
         'pringles1',
         'pringles2',
         'bifrutas_tropical_can',
         'biscuits_pack',
         'cup_glass_new',
         'cup_paper',
         'peroni',
         'plastic_cup',
         'tea_box'
        ]

banner = """
=================================================
 _       __      _ __            ____        __ 
| |     / /___ _(_) /____  _____/ __ )____  / /_
| | /| / / __ `/ / __/ _ \/ ___/ __  / __ \/ __/
| |/ |/ / /_/ / / /_/  __/ /  / /_/ / /_/ / /_  
|__/|__/\__,_/_/\__/\___/_/  /_____/\____/\__/  
                                                
=================================================
"""

welcome_msg = 'Hello, I am a tiago waiter.\nWhat would you like to order?'

rospy.init_node('request_order_node')
order_pub = rospy.Publisher('/waitbot/orderList', String, queue_size=5)

def typewriter(msg):
    for char in msg:
        sleep(0.1)
        sys.stdout.write(char)
        sys.stdout.flush()

def print_items(items):
    msg = items[0]
    for i in range(1, len(items)):
        print (msg, end="\r")
        sleep(0.3)
        msg += ' ' + items[i]

    print('')

def get_order():
    os.system('clear')
    print(banner)

    typewriter(welcome_msg)
    print('\n')

    print('CATALOG')
    print_items(items)

    order = []

    while len(order) < 3:
        order_str = input('Order item: ').strip().lower()

        if order_str not in items:
            print(order_str + ' is not available. Please order something else')
        else:
            order.append(order_str)
            print('current order: ' + ', '.join(order))
    
    print('\nYou ordered: ' + ', '.join(order))
    valid = input('If your order is correct press ENTER or press anything to order again:\n')

    if valid == '':
        return order
    elif valid.lower() == 'q':
        return 'break'

while True:
    answer = get_order()

    if type(answer) == list:
        order_pub.publish(json.dumps(answer))
    elif answer == 'break':
        break