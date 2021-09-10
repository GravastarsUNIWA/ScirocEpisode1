#!/usr/bin/python

import rospy
import json
from std_msgs.msg import String,Bool

class process_detections:
	"""docstring for process_detections"""
	def __init__(self):
		rospy.init_node('process_detections')
		rospy.loginfo("Node /process_detections initiated")
		self.detections_sub = rospy.Subscriber("/object_detection/counter", String, self.process_detections_callback)
		self.people_counter_pub = rospy.Publisher('/object_detection/people_counter', String, queue_size=1)
		self.isFood_pub = rospy.Publisher('/object_detection/isFood', Bool, queue_size=1)

		self.objs =['beer',
					'cocacola',
					'plastic_cup',
					'bifrutas_tropical_can',
					'biscuits_pack',
					'sprite',
					'pringles1',
					'pringles2',
					'peroni',
					'tea_box',
					'estathe',
					'cup',
					'wine',
					'bottle']

	def process_detections_callback(self, data):

		try:
			
			# get people
			people_counter = json.loads(data.data)['person']
			self.people_counter_pub.publish(str(people_counter))

		except KeyError:
			self.people_counter_pub.publish(str(0))
			pass

		detections = json.loads(data.data)
		# get everything except people (food) 
		objsSet = set(self.objs)
		exclude_keys=["person"]
		no_people_dictSet = set({k: detections[k] for k in set(list(detections.keys())) - set(exclude_keys)})

		if objsSet.intersection(no_people_dictSet):
			# if any obj is detected
			print(objsSet.intersection(no_people_dictSet))
			print("true")
			self.isFood_pub.publish(True)
		else:
			self.isFood_pub.publish(False)
			print("false")

if __name__ == '__main__':

    process_detections()
    rospy.spin()