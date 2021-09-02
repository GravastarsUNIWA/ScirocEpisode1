#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from os import stat
import re
import nltk
import time
import string
import random

from word2number import w2n

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import rospy
from waitbot.msg import speech_recognition
from std_msgs.msg import String
from std_msgs.msg import Bool


#region Phrases & Responses

greeting_phrase = [
    "Hello! I am waitbot! Don't worry i won't make you wait! Are you ready to order?"]
confused_phrase = ["i didn't catch that, can you please repeat",
                   "it may be the noise, i may need a recharge but my mics didn't understand what you said", "i didn't get that, can you please repeat"]
rephrase = [
    "i am having a difficult time to understand what you said. please rephrase your sentence"]

order_more_phrase = ["would you like anything else", "can i get you anything else"]

"""---------------------------------------------------------------------------------------------------------------------------------------------------------"""

items_patterns = ["which items do you have",
                  "what kinds of items are there", "what do you sell"]
items_responses = ["we sell", "we have"]

order_patterns = ["i want a", "could you bring me a", "i would like to order a", "i would like a"]
order_responses = ["did you order a ", "is your order a"]

confirmation_patterns = ["that is correct", "yes", "yes please","that is what i ordered", "exactly", "perfect", "ok", "correct", "okay", "of course"]

disagreement_patterns = ["no","nop", "nope ", "cancel", "negative", "i don't want anything else", "no please", "i am okay", "not ready"]

confirmation_responses = [
    "thank you for your cooperation", "thank you", "ok", "got it", "noted that"]

correction_patterns = ["no i ordered a ", "no this is not what i ordered"]
correction_responses = [
    "thank you for your help", "thank you for correcting that "]

greeting_patterns = ["hi", "hey", "how are you",
                     "is anyone there", "hello", "good day", "good morning"]
greeting_responses = ["hello, how could i help you?",
                      "hello, what can i get you?", "hello, are you ready to order?"]

goodbye_patterns = ["bye", "see you later", "goodbye"]
goodbye_responses = ["see you later, thanks for visiting",
                     "have a nice day", "bye come back again soon."]

thanks_patterns = ["thanks", "thank you", "that's helpful", "thanks a lot"]
thanks_responses = ["happy to help", "any time", "my pleasure"]

order_request_patterns = ["i would like to order", "we would like to order"
                          "could i order please", "could you take my order ", "can i order", "can we order"]
order_request_responses = [ "i am all ears", "someone is hungry so you'd better start quickly!"]

order_more_request_responses = ["please tell me", "i am all ears","i hear you"]
#    "please tell me", "what would you like to order", "of course", "i am all ears", "i am ready to hear your order",
#                "someone is hungry so you'd better start quickly!"]

patterns = [greeting_patterns, order_request_patterns,items_patterns, order_patterns, confirmation_patterns, disagreement_patterns, thanks_patterns, goodbye_patterns]

#endregion 

#region Item Categories

drinks = ["soft drinks", "juice", "coffee", "water", "alcoholic", "milk"]

softDrinks = ["coke", "sprite", "tea"]

coke = ["cola", "coke", "cocacola", "coca cola", "pepsi"]

sprite = ["sprite", "mountain dew", "seven up", "soda"]

juice = ["bifrutas", "juice"]

coffee = ["coffee", "cappuccino"]

tea = ["tea", "estathe"]

water = ["water"]

alcoholic = ["wine", "beer"]

milk = ["milk"]
foods = ["baked potatoes", "fried potatoes", "pringles", "chips",
         "biscuits", "cracker", "sandwich", "chewing, gum", "ice cream"]
pcs = ["glass", "plastic cup", "pack", "bottle",
       "bottles", "can", "cup", "packet", "packets","piece", "cans", "box"]

modifiers = ["red", "white", "green", "hot", "cold", "draft", "macchiato",
             "late", "fruit", "orange", "tropical", "tap" "sparkling", "lemon", "peroni"]

misc = ["napkin", "wc", "chewing gum"]
numbers = ["one", "two", "three", "four", "five",
           "six", "seven", "eight", "nine", "ten"]

#endregion

#region Fuzzy Wuzzy how to
# Fuzzy Wuzzy string matching

# ratio()
# function calculate the Levenshtein distance similarity ratio between the two strings (sequences).
# We can say the Str_B has a similarity of 93% to Str_A when both are lowercase.


# partial ratio()
# function allows us to perform substring matching.
# This works by taking the shortest string and matching it with all substrings that are of the same length.

# token_sort_ratio()
# function sorts the strings alphabetically and then joins them together.
# Then, the fuzz.ratio() is calculated. This can come in handy when the strings you are comparing are the same in spelling but are not in the same order.

# token_set_ratio()
# function is similar to the token_sort_ratio() function above, except it takes out the common tokens before calculating the fuzz.ratio()
# between the new strings. This function is the most helpful when applied to a set of strings with a significant difference in lengths.

# process, that returns the strings along with a similarity score out of a vector of strings.
# All you need to do is call the extract() function after process.


# print(fuzz.partial_ratio(phrase2,phrase1))
# print(fuzz.ratio(phrase1,phrase2))
# print(fuzz.token_sort_ratio(phrase1,phrase2))
# print(fuzz.token_set_ratio(phrase1,phrase2))

#testing_phrase = "hello can i make an order"
#testing_phrase = "yes we are ready to order"

#phrase = testing_phrase

#endregion

#region Variables
maxRatio = 0
maxList = 0
maxSublist = 0

ilist = 0
isublist = 0

state = 0
substate = 0

previous_state = 0
table_ready_to_be_served = True

isOrdering = False
isPattern = False

time_elapsed = 0
time_spoken = 0
time_now = 0
time_silence = 0
time_waiting = 0

timetoWait = 10
timetoSpeak = 20

sr_isRecognized = False
final_sr = " "

answer = " "
nlp_phrase = " "

hasSpoken = True

last_msg = ""
last_msg_time = 0
phraseIsNew = False

orderList = []
have_asked = False

customer_isSpeaking = False
tts_isSpeaking = False

tts_phrase = ""

#endregion

#region Speech Recognition & NLP stuff
def sr_listener():

    global sr_isRecognized, final_sr, phraseIsNew, time_spoken

    rospy.init_node('nlp_parser', anonymous=True)

    rospy.Subscriber('/waitbot/speech_recognizer', speech_recognition, getPhrase)

def getPhrase(msg):

    global sr_isRecognized, final_sr, state, answer, last_msg, phraseIsNew, time_spoken, customer_isSpeaking, last_msg_time

    phraseIsNew = False

    #In case there is a final result
    if msg.partial_result == "None" and msg.final_result != "None":
        if msg.time_recognized.secs != last_msg_time:
            sr_isRecognized = msg.isSpeech_recognized
            #partial_sr = msg.partial_result
            final_sr = msg.final_result
            last_msg_time = msg.time_recognized.secs
            time_spoken = time.time()
            phraseIsNew = True
            customer_isSpeaking = False
            rospy.loginfo(rospy.get_caller_id() + "\nCustomer said:  %s", final_sr)
        else:
            phraseIsNew = False
    
    
    #In case there is a partial result
    if msg.partial_result != "None" and msg.final_result == "None": 
        customer_isSpeaking = True
        final_sr = "None"
        partial_sr = msg.partial_result
        phraseIsNew = False
    else:
        customer_isSpeaking = False
        phraseIsNew = False

    last_msg = final_sr

def parsePhrase(final_sr):
   
    #region Check if the said phrase is an order item
    global drinks, softDrinks, coke, sprite, juice, coffee, tea, water, alcoholic, milk, foods, pcs, modifiers, misc, numbers

    global nlp_phrase, isOrdering, isPattern
    
    isOrdering = False
    isPattern = False
    
    qty = 0
    categ = "none"
    item = "none"
    packet_type = "none"
    mod = "none"

    percentage = 80

    stop_words = set(stopwords.words('english'))

    input_str = final_sr

    input_str = input_str.lower()  # make everything lowercase

    # removes punctuation such as {}[] and so on
    input_str = input_str.translate(str.maketrans('', '', string.punctuation))

    tokens = word_tokenize(input_str)

    text = nltk.word_tokenize(input_str)

    phrase = input_str #This variable will be used to determine if the said phrase matches with some of the other phrases

    # TODO
    #filtered_sentence = []
    #
    # for w in text:
    #    if w not in stop_words:
    #        filtered_sentence.append(w)
    #
    # print(filtered_sentence)
    #pos = nltk.pos_tag(filtered_sentence)

    pos = nltk.pos_tag(text)

    # Loop into all the chunks and find all the info needed

    for i in range(len(pos)):

        wasFound = False

        word, pos_tag = pos[i]

        # print(word,"+",pos_tag)

        # Search if the word is a number, if yes make it a real number
        if pos_tag == 'CD':
            isNumeric = True
            qty = w2n.word_to_num(word)

        else:
            # Determine the type of order

            for drink in drinks:

                # Soft drinks
                if drink == "soft drinks":
                    for soft in softDrinks:
                        if soft == "coke":
                            for alt in coke:
                                if alt == word:
                                    categ = drink
                                    item = "coke"
                                    wasFound = True
                                    break
                            if wasFound == True:
                                break
                        if wasFound == True:
                            break

                        if soft == "sprite":
                            for alt in sprite:
                                if alt == word:
                                    categ = drink
                                    item = "sprite"
                                    wasFound = True
                                    break
                            if wasFound == True:
                                break
                        if wasFound == True:
                            break

                        if soft == "tea":
                            for alt in tea:
                                if alt == word:
                                    categ = drink
                                    item = "tea"
                                    wasFound = True
                                    break
                            if wasFound == True:
                                break
                        if wasFound == True:
                            break
                    if wasFound == True:
                        break

                elif drink == "juice":
                    for jc in juice:
                        if jc == word:
                            categ = drink
                            item = word
                            wasFound = True
                            break
                        if wasFound == True:
                            break
                    if wasFound == True:
                        break

                elif drink == "juice":
                    for jc in juice:
                        if jc == word:
                            categ = drink
                            item = word
                            wasFound = True
                            break
                        if wasFound == True:
                            break
                    if wasFound == True:
                        break

                elif drink == "coffee":
                    for typ in coffee:
                        if typ == word:
                            categ = drink
                            item = word
                            wasFound = True
                            break
                        if wasFound == True:
                            break
                    if wasFound == True:
                        break

                elif drink == "tea":
                    for typ in tea:
                        if typ == word:
                            categ = drink
                            item = word
                            wasFound = True
                            break
                        if wasFound == True:
                            break
                    if wasFound == True:
                        break

                elif drink == "water":
                    for typ in water:
                        if typ == word:
                            categ = drink
                            item = word
                            wasFound = True
                            break
                        if wasFound == True:
                            break
                    if wasFound == True:
                        break

                elif drink == "alcoholic":
                    for typ in alcoholic:
                        if typ == word:
                            categ = drink
                            item = word
                            wasFound = True
                            break
                        if wasFound == True:
                            break
                    if wasFound == True:
                        break

            # Search if the item is on foods
            if wasFound == False:
                for food in foods:
                    if food == word:
                        categ = "foods"
                        item = word
                        wasFound = True
                        break
                    if wasFound == True:
                        break
                if wasFound == True:
                    break

            # Search if the word is reffering to unit type
            if wasFound == False:
                for piece in pcs:
                    if piece == word:
                        packet_type = piece
                        wasFound = True
                        break
                    if wasFound == True:
                        break
            # Search if the word is reffering to modifier type
            if wasFound == False:
                for modifier in modifiers:
                    if modifier == word:
                        mod = word
                        wasFound = True
                        break
                    if wasFound == True:
                        break

    if qty == 0:
        qty = 1


    if ((categ == "none") and (item == "none")):
        #region Check if the said phrase matches a pattern phrase
        global patterns, maxRatio, ratioSet, maxList, state
        ilist = 0
        maxList =  0
        maxRatio = 0

        # make a quick search for in every possible pattern
        for pattern in patterns:

            # print(fuzz.partial_ratio(phrase,pattern))
            # print(fuzz.ratio(phrase,pattern))
            # print(fuzz.token_sort_ratio(phrase,pattern))

            ratioSet = fuzz.token_set_ratio(phrase, pattern)

            #print("")
            #print("Pattern Set Ratio:  " + str(ratioSet))
            #print("")

            if maxRatio < ratioSet:
                maxRatio = ratioSet
                maxList = ilist

            ilist = ilist + 1
            isublist = 0

            for subpattern in pattern:
                isublist = isublist + 1

                #print(" ")
                #print(phrase)
                #print(subpattern)

                ratio = fuzz.ratio(subpattern, pattern)
                #print("Ratio:  " + str(ratio))

                ratioPartial = fuzz.partial_ratio(subpattern, phrase)
                #print("Partial Ratio:  " + str(ratioPartial))

                ratioSort = fuzz.token_sort_ratio(subpattern, phrase)
                #print("Sort Ratio:  " + str(ratioSort))

                ratioSet = fuzz.token_set_ratio(subpattern, phrase)
                #print("Set Ratio:  " + str(ratioSet))

        # search in every possible sub pattern for the exact match...! testing only
        
        #TODO
        #print("\nMaximum similarity comes from the bag of words: " + str(maxList))
        #print(patterns[maxList])
        
        isOrdering = False
        isPattern =  True
        
        return maxList
        #endregion
    else:
        isOrdering = True
        isPattern = False

        print("Cutomer would like: ")
        print("Category: ", categ, " | Item: ", item, " | Modifier: ", mod, " | Unit: ", packet_type, " | Qty: ", qty)
        
        return (categ+";"+item+";"+mod+";"+packet_type+";"+str(qty))
    #endregion

#endregion 

def say(phrase):

    print("")
    print("Waitbot says: " + phrase)
    print("")

    pubPhrase.publish(phrase)
    #print("Published phrase to topic")

def state_retrieval(pattern):
    global previous_state, table_ready_to_be_served, state, substate, isOrdering, time_waiting, timetoSpeak, phraseIsNew, orderList, have_asked

    #patterns = [greeting_patterns, order_request_patterns, items_patterns, order_patterns, confirmation_patterns, disagreement_patterns, thanks_patterns, goodbye_patterns]
    #pattern: 20 -> ordering 
    #pattern: 21 -> hearing whatever

    # Robot greets and introduces itself
    if (state == 0) and (table_ready_to_be_served == True) and (isPattern == True):
        if substate == 0:
            state = 1 # Introduce yourself when in front of the table
            if (pattern == "nothing"): 
                say(random.choice(greeting_phrase))
            elif (pattern == 0):
                say(random.choice(greeting_phrase)) #Greetings, Are you ready to order?
        
    # Robot waits for confirmation on ordering
    elif (state == 1) and (isPattern == True): 
        if substate == 0:
            if (pattern == 1 or pattern == 4 ): # Customers would like to order
                say(random.choice(order_request_responses)) # Something like i am ready to take your order
                previous_state = state
                state = 2   
            elif (pattern == 5): # Customers are not ready to order yet
                previous_state = state
                time_waiting = time.time()
                say("okay, i will be back soon!")
                substate = 2 #Wait until they are ready to order       
        
        elif substate == 2:
            #print (time.time() - time_waiting)
            if (time.time() - time_waiting) >= timetoWait:
                say("Are you ready to order now?")
                substate = 0
            if pattern == 1:
                say(random.choice(order_request_responses)) # Something like i am ready to take your order
                previous_state = state
                substate = 0
                state = 2  


    
    elif (state == 2):
        #print (time.time() - time_spoken)
        # If that was said was an item order write it down
        if pattern == 20:
            print (st) 
            orderList.append(st)
            substate = 1
            have_asked = False
        elif pattern == 21:
            pass

        #If some time has passed from the last ordered item, ask if they would like something else
        if (time.time() - time_spoken) >= timetoSpeak: 
            if substate == 0 and have_asked == False:
                say("I am waiting for your order")
                have_asked = True
            #TODO in case we have asked and a long time have passed
            if substate == 1 and have_asked == False:
                say(random.choice(order_more_phrase))
                have_asked = True
            if substate == 1 and have_asked == True and (time.time() - time_spoken) >= 60:
                say("You have stopped speaking to me, so i assume that you are done with your order! Have a good one!")
                have_asked = False
                substate = 0
                state = 3        
        
        if substate == 1:
            if (pattern == 1 or pattern == 3 or pattern == 4): #If customer wants to order more
                say("I am all ears!")
            if (pattern == 5 or pattern==6):
                say(random.choice(confirmation_responses))
                substate = 0
                state = 3

    elif (state == 3):
        if substate == 0:
            substate = 1
            say("you have ordered")
            for item in orderList:
                say(item)
        if substate == 1:
            state = 0
            substate = 0

    return state


if __name__ == '__main__':

    try:
        pubPhrase = rospy.Publisher('waitbot/tts/phrase', String, queue_size=5)
        while not rospy.is_shutdown():
            
            sr_listener()    

            if phraseIsNew == True:

                st = parsePhrase(final_sr)

                if (isOrdering == True):
                    state = state_retrieval(20)
                elif (isPattern == True): 
                    state = state_retrieval(st)
            else:
                state = state_retrieval(21)

    except KeyboardInterrupt:
        rospy.loginfo("Stopping npl parser...")
        rospy.sleep(1)
        print("node terminated")

#TODO If there is no package selected, ask which package would the customer like