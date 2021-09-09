#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import rospkg
from waitbot.msg import speech_recognition
from std_msgs.msg import String, Bool

   
def speech_publisher(str):
    msg = speech_recognition()   
    isRecognized = False
    msg.isSpeech_recognized = True
    msg.time_recognized = rospy.Time.now()
    msg.final_result = str
    msg.partial_result = "None"
    pub.publish(msg)

if __name__ == '__main__':
    
    try:
        pub = rospy.Publisher('waitbot/speech_recognizer', speech_recognition, queue_size=10)
        node_name = "vosk_speech_recognizer_txt"
        rospy.init_node(node_name, anonymous=False)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            
            text = input("write here your message: ")
            if text:
                speech_publisher(text)
            
    except (KeyboardInterrupt, rospy.ROSInterruptException) as e:
        rospy.loginfo("Stopping the text node...")
        rospy.sleep(1)
        print("node terminated")
