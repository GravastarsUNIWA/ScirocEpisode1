#!/usr/bin/env python3


from os import stat
import re
import nltk
import time
import string
import random
import json
from nltk.corpus.reader import wordlist

from word2number import w2n

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import rospy
from waitbot.msg import speech_recognition
from std_msgs.msg import String
from std_msgs.msg import Bool

# region Phrases & Responses



class NLP():

    def __init__(self):

        self.greeting_phrase = [
            "Hello! Are you ready to order?"]
        self.confused_phrase = ["i didn't catch that, can you please repeat",
                           "it may be the noise, i may need a recharge but my mics didn't understand what you said", "i didn't get that, can you please repeat"]
        self.rephrase = [
            "i am having a difficult time to understand what you said. please rephrase your sentence"]

        self.order_more_phrase = ["would you like anything else",
                             "can i get you anything else"]

        self.items_patterns = ["which items do you have",
                          "what kinds of items are there", "what do you sell"]

        self.items_responses = ["we sell", "we have"]

        self.order_patterns = ["i want a", "could you bring me a",
                          "i would like to order a", "i would like a"]
        self.order_responses = ["did you order a ", "is your order a"]

        self.confirmation_patterns = ["that is correct", "yes", "yes please", "i am",
                                 "that is what i ordered", "exactly", "perfect", "ok", "yeah", "correct", "okay", "of course"]

        self.disagreement_patterns = ["no", "nop", "nope ", "cancel", "negative",
                                 "i don't want anything else", "no please", "not ready"]

        self.confirmation_responses = [
            "thank you for your cooperation", "thank you", "ok", "got it", "noted that"]

        self.correction_patterns = ["no i ordered a ", "no this is not what i ordered"]

        self.correction_responses = [
            "thank you for your help", "thank you for correcting that "]

        self.greeting_patterns = ["hi", "hey", "how are you",
                             "is anyone there", "hello", "good day", "good morning"]
        self.greeting_responses = ["hello, how could i help you?",
                              "hello, what can i get you?", "hello, are you ready to order?"]

        self.goodbye_patterns = ["bye", "see you later", "goodbye"]
        self.goodbye_responses = ["see you later, thanks for visiting",
                             "have a nice day", "bye come back again soon."]

        self.thanks_patterns = ["thanks", "thank you", "that's helpful", "thanks a lot","that's it", "that's all", "that is all"]
        self.thanks_responses = ["happy to help", "any time", "my pleasure"]

        self.order_request_patterns = ["i would like to order", "we would like to order"
                                  "could i order please", "could you take my order ", "can i order", "can we order"]
        self.order_request_responses = ["i am all ears",
                                   "someone is hungry so you'd better start quickly!"]

        self.order_more_request_responses = [
            "please tell me", "i am all ears", "i hear you"]

        self.patterns = [self.greeting_patterns, self.order_request_patterns, self.items_patterns, self.order_patterns,
                    self.confirmation_patterns, self.disagreement_patterns, self.thanks_patterns, self.goodbye_patterns]

        self.item_list = {"cocacola"  : ["cola", "coke", "cocacola", "coca cola", "pepsi"],
                     "sprite"    : ["sprite", "mountain dew", "seven up", "soda", "sprites"],
                     "coffee"    : ["coffee", "cappuccino"],
                     "tea"       : ["tea", "estathe"],
                     "juice"     : ["bifrutas", "juice"],
                     "wine"      : ["wine"],
                     "beer"      : ["beer"],
                     "milk"      : ["milk"],
                     "water"     : ["water"],
                     "pringles"  : ["chips","chip","pringle", "pringles", "potato chips", "potato"],
                     "biscuits"  : ["biscuits", "biscuit"],
                     "modifiers" : ["red", "white", "green", "hot", "cold", "draft", "macchiato",
                                    "late", "fruit", "orange", "tropical", "tap" "sparkling", "lemon", "peroni"]
                     }


        self.state = 0
        self.substate = 0

        self.previous_state = 0
        self.table_ready_to_be_served = True

        self.isOrdering = False
        self.isPattern = False

        self.time_elapsed = 0
        self.time_spoken = 0
        self.time_now = 0
        self.time_silence = 0
        self.time_waiting = 0

        self.timetoWait = 10
        self.timetoSpeak = 20

        self.sr_isRecognized = False
        self.final_sr = " "

        self.answer = " "
        self.nlp_phrase = " "

        self.hasSpoken = True

        self.last_msg = ""
        self.last_msg_time_secs = 0
        self.last_msg_time_nsecs = 0
        self.phraseIsNew = False

        self.orderList = []
        self.have_asked = False

        self.customer_isSpeaking = False
        self.tts_isSpeaking = False

        self.tts_phrase = ""
        self.pattern = 0

        self.percentage = 80

        self.stop_words = set(stopwords.words('english'))


        self.sr_sub = rospy.Subscriber('/waitbot/speech_recognizer',
                     speech_recognition, self.getPhrase_callback)
        self.orderList_pub = rospy.Publisher(
            '/waitbot/orderList', String, queue_size=1)
        self.pubPhrase = rospy.Publisher('waitbot/tts/phrase', String, queue_size=5)
        rospy.sleep(0.1)

        self.readytoorder_sub = rospy.Subscriber('/table_status/ready',Bool, self.tableReady_callback)


    def tableReady_callback(self, msg):
        if msg.data == True:
            self.state_retrieval(None)
            

    def getPhrase_callback(self, msg):

        # In case there is a final result
        if msg.partial_result == "None" and msg.final_result != "None":
            if (msg.time_recognized.secs != self.last_msg_time_secs) and (msg.time_recognized.nsecs != self.last_msg_time_nsecs):
                self.sr_isRecognized = msg.isSpeech_recognized
                #partial_sr = msg.partial_result
                self.final_sr = msg.final_result
                self.last_msg_time_secs = msg.time_recognized.secs
                self.last_msg_time_nsecs = msg.time_recognized.nsecs
                self.time_spoken = time.time()
                self.phraseIsNew = True

                rospy.loginfo(rospy.get_caller_id() +" Customer said:  %s", self.final_sr)
                state = self.state_retrieval(self.parsePhrase(self.final_sr))
            else:
                self.phraseIsNew = False

        # In case there is a partial result
        if msg.partial_result != "None" and msg.final_result == "None":
            self.final_sr = "None"
            self.partial_sr = msg.partial_result
            self.phraseIsNew = False
        else:
            self.phraseIsNew = False

        self.last_msg = self.final_sr

    def parsePhrase(self, final_sr):
        input_str = final_sr
        input_str = input_str.lower() 

        input_str = input_str.translate(str.maketrans('', '', string.punctuation))
        # print(input_str)

        text = nltk.word_tokenize(input_str)

        pos = nltk.pos_tag(text)
        mod = None
        item = None
        phrase = input_str
        ilist = 0
        maxRatio = 0
        qty = 0

        for i in range(len(pos)):

            wasFound = False
            word, pos_tag = pos[i]

            if pos_tag == 'CD':
                qty = w2n.word_to_num(word)

            else:
                for key in self.item_list.keys():
                    for itm in self.item_list.get(key):
                        if itm == word:
                            wasFound = True
                            if key == "modifiers":
                                mod = itm
                            else:
                                #categ = key
                                item = key
                            break
                    if wasFound == True:
                        break


        if ((mod == None) and (item == None)):

            for pattern in self.patterns:

                ratioSet = fuzz.token_set_ratio(phrase, pattern)

                if maxRatio < ratioSet:
                    maxRatio = ratioSet
                    maxList = ilist

                ilist += 1

            self.isOrdering = False
            self.isPattern = True

            if maxRatio <= 30:
                # maxList = 10 eipes papatza
                maxList = 10
            return maxList


        else:
            self.isOrdering = True
            self.isPattern = False
            if qty == 0:
                qty = 1

            print("Cutomer would like: ")
            print( " | Qty: ", qty, " | Modifier: ", mod, "| Item: ", item)

            #TODO Decide the return order
            #return (item+";"+mod+";"+packet_type+";"+str(qty))

            if mod != None and item != None:
                item = mod + " " + item

            return item

    def say(self, phrase):

        # self.phrase = phrase

        print("")
        print("Waitbot says: " + phrase)
        print("")

        self.pubPhrase.publish(phrase)

        #print("Published phrase to topic")

    def state_retrieval(self, pattern):
        # Robot greets and introduces itself
        #if (self.state == 0) and (self.table_ready_to_be_served == True) and (self.isPattern == True):
        if (self.state == 0):
            if self.substate == 0:
                if (pattern == None):
                    self.state = 1 # Introduce yourself when in front of the table
                    self.say(random.choice(self.greeting_phrase))
                # else:
                #     if self.isPattern == True:
                #         if (pattern == 0):
                #             self.state = 1 # Introduce yourself when in front of the table
                #             self.say(random.choice(self.greeting_phrase)) #Greetings, Are you ready to order?
                #         elif pattern == 10:
                #             self.say(random.choice(self.confused_phrase))

        # Robot waits for confirmation on ordering
        elif (self.state == 1) and (self.isPattern == True):
            if self.substate == 0:
                if (pattern == 1 or pattern == 4 ): # Customers would like to order
                    self.say(random.choice(self.order_request_responses)) # Something like i am ready to take your order
                    self.previous_state = self.state
                    self.state = 2
                elif (pattern == 5): # Customers are not ready to order yet
                    self.previous_state = self.state
                    self.time_waiting = time.time()
                    self.say("okay, i will be back soon!")
                    self.substate = 2 #Wait until they are ready to order
                elif pattern == 10:
                    self.say(random.choice(self.confused_phrase))

            elif self.substate == 2:
                #print (time.time() - time_waiting)
                if (time.time() - self.time_waiting) >= self.timetoWait:
                    self.say("Are you ready to order now?")
                    self.substate = 0
                if pattern == 1:
                    self.say(random.choice(self.order_request_responses)) # Something like i am ready to take your order
                    self.previous_state = self.state
                    self.substate = 0
                    self.state = 2

        elif (self.state == 2):
            #print (time.time() - time_spoken)
            # If that was said was an item order write it down
            if isinstance(pattern, str):
                self.orderList.append(pattern)
                self.substate = 1
                self.have_asked = False
            elif pattern == 10:
                self.say(random.choice(self.confused_phrase))


            #If some time has passed from the last ordered item, ask if they would like something else
            if (time.time() - self.time_spoken) >= self.timetoSpeak:
                if self.substate == 0 and self.have_asked == False:
                    self.say("I am waiting for your order")
                    self.have_asked = True
                if self.substate == 1 and self.have_asked == False:
                    self.say(random.choice(self.order_more_phrase))
                    self.have_asked = True
                if self.substate == 1 and self.have_asked == True and (time.time() - self.time_spoken) >= 60:
                    self.say("You have stopped speaking to me, so i assume that you are done with your order! Have a good one!")
                    self.have_asked = False
                    self.substate = 0
                    self.state = 3

            if self.substate == 1:
                if (pattern == 1 or pattern == 3 or pattern == 4): #If customer wants to order more
                    self.say("I am all ears!")
                    self.substate = 0
                if (pattern == 5 or pattern==6):
                    #final state
                    self.substate = 0
                    # self.state = 3
                    self.say(random.choice(self.confirmation_responses))                 
                    self.say("you have ordered")
                    self.orderList_pub.publish(json.dumps(self.orderList))
                    for item in self.orderList:
                        self.say(item)

                    self.orderList = []
                    self.state = 0
                    self.substate = 0
                    self.say("i'll be back! soon with your order!")

        return self.state


if __name__ == '__main__':
    try:
        rospy.init_node('nlp_parser', anonymous=True)
        obj = NLP()
        # c.run()
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Stopping npl parser...")
        #rospy.sleep(1)
        print("node terminated")
