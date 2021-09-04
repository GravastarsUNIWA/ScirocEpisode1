#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from os import stat
import string
import random

from word2number import w2n

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import rospy
from waitbot.msg import speech_recognition
from std_msgs.msg import String
from std_msgs.msg import Bool

import pyttsx3


def tts_onStart( name):
    print('starting speaking', name)
    publish_status(True)

def tts_onWord( name, location, length):
    print('word', name, location, length)

def tts_onEnd( name, completed):
   print ('finishing speaking', name, completed)
   publish_status(False)
   engine.endLoop()


def publish_status( isSpeaking):
    # Make the status true if it is speaking and false if it is not

    if isSpeaking == True:
        rospy.sleep(1)
        pubStatus.publish(True)
        print("Published!")#TODO
    else:
        rospy.sleep(1)
        pubStatus.publish(False)
        print("Published!")#TODO

def say( phrase):

    print("")
    print("Waitbot says: " + phrase)
    print("")

    engine = pyttsx3.init()
    engine.connect('started-utterance', tts_onStart)
    #engine.connect('started-word', tts_onWord)
    engine.connect('finished-utterance', tts_onEnd)
    engine.say(phrase,"tts_engine")
    #engine.startLoop() 
    engine.runAndWait()

    


def callback( msg):
    phrase = msg.data
    say(phrase)

def ros_init():

    rospy.init_node('tts_engine', anonymous=True)
    rospy.Subscriber("waitbot/tts/phrase", String, callback)
    rospy.spin()    

if __name__ == '__main__':

    try:
        pubStatus = rospy.Publisher('waitbot/tts/status', Bool, queue_size=0)
        ros_init()
        


    except KeyboardInterrupt:
        rospy.loginfo("Stopping tts engine...")
        rospy.sleep(1)
        print("node terminated")