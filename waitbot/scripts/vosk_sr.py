#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Angelo Antikatzidis
# Software as a part for my thesis at University of West Attica, Automation engineering department

import argparse
import array
import json
from mmap import MAP_SHARED
import os
import queue
import sys
import time
from pathlib import Path
from threading import Lock

import sounddevice as sd
import vosk

import rospy
import rospkg
from waitbot.msg import speech_recognition
from std_msgs.msg import String, Bool

rospack = rospkg.RosPack()
rospack.list()
package_path = rospack.get_path('waitbot')

q = queue.Queue()

model_path = "/models/"
model_name = "model-en"
model_dir = package_path + model_path + model_name


tts_status = False

def callback(indata, frames, time, status):
    #"""This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def tts_get_status(msg):
    global tts_status
    tts_status = msg.data
    #rospy.loginfo(rospy.get_caller_id() + "\nTTS status is:  %s", tts_status)

def tts_status_listenner():
    rospy.Subscriber("waitbot/tts/status", Bool, tts_get_status)

def speech_recognizer():

    # ROS node initialization
    pub = rospy.Publisher('waitbot/speech_recognizer', speech_recognition, queue_size=10)
    node_name = "vosk_speech_recognizer"
    rospy.init_node(node_name, anonymous=False)
    rate = rospy.Rate(100)  # 10hz

    rospy.on_shutdown(cleanup)

    msg = speech_recognition() 

    input_dev_num = sd.query_hostapis()[0]['default_input_device']
    if input_dev_num == -1:
        rospy.logfatal('No input device found')
        raise ValueError('No input device found, device number == -1')
    
    device_info = sd.query_devices(input_dev_num, 'input')
    # soundfile expects an int, sounddevice provides a float:
    samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(model_dir)
    
    try:
        with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=input_dev_num, dtype='int16',
                               channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)
            
            rec = vosk.KaldiRecognizer(model, samplerate)
            
            isRecognized = False
            isRecognized_partially = False
            
            while not rospy.is_shutdown():
                
                tts_status_listenner()
                
                if tts_status == True:
                    # If the text to speech is operating, clear the queue 
                    with q.mutex:
                        q.queue.clear()
                
                elif tts_status == False:

                    data = q.get()
                    
                    if rec.AcceptWaveform(data):
                        # In case of final result
                                     
                        res = rec.FinalResult()

                        #result = rec.Result()
                        #print(result)

                        diction = json.loads(res)
                        lentext = len(diction["text"])
                        
                        if lentext > 2:
                            result_text = diction["text"]
                            #result_res  = diction["result"] #Not needed for the time being
                            
                            print(result_text)
                            
                            isRecognized = True

                        else:
                            isRecognized = False
                        #TODO
                        with q.mutex:
                            q.queue.clear()

                    else:
                        # In case of partial result

                        result_partial = rec.PartialResult()
                        
                        if (len(result_partial) > 20):
                            #DEBUGprint (result_partial)
                            isRecognized_partially = True
                            partial_dict = json.loads(result_partial)
                            partial = partial_dict["partial"]


                    if (isRecognized is True):
                        
                        isRecognized = False
                        # Build the message
                        msg.isSpeech_recognized = True
                        msg.time_recognized = rospy.Time.now()
                        msg.final_result = result_text
                        msg.partial_result = "None"

                        pub.publish(msg)

                        
                    elif (isRecognized_partially is True):
                        if partial != "None":
                            msg.isSpeech_recognized = False
                            msg.time_recognized = rospy.Time.now()
                            msg.final_result = "None"
                            msg.partial_result = partial
                            pub.publish(msg)
                            partial = "None"
                            isRecognized_partially = False

    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
    except KeyboardInterrupt:
        rospy.loginfo("Stopping the vosk speech recognition node...")
        rospy.sleep(1)
        print("node terminated")


def cleanup():
    print("Shutting down vosk_speech_recognizer node.")


def main():
    try:
        speech_recognizer()
        rospy.spin()
    except (KeyboardInterrupt, rospy.ROSInterruptException) as e:
        rospy.loginfo("Stopping the vosk speech recognition node...")
        rospy.sleep(1)
        print("node terminated")


if __name__ == '__main__':
    main()
