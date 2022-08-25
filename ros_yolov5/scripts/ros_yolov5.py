#!/home/paris/miniconda3/envs/venv/bin/python

import json
import os
import cv2
import numpy as np
from collections import Counter
import torch

import rospy
import rospkg

from std_msgs.msg import String, UInt8MultiArray
from sensor_msgs.msg import Image
# from ros_yolov5.msg import DetectedObject, DetectedObjectNames, DetectionCount, DetectionResult

class ObjectDetector:

    def draw_text(self, img, text,
          font=cv2.FONT_HERSHEY_PLAIN,
          pos=(0, 0),
          font_scale=1,
          font_thickness=2,
          text_color=(255, 255, 255),
          text_color_bg=(255, 0, 0)
          ):

        """
        https://stackoverflow.com/questions/60674501/how-to-make-black-background-in-cv2-puttext-with-python-opencv
        """
        x, y = pos
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
        cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

        return text_size

    def image_callback(self, msg):
        names = self.model.names
    
        # Hack for getting image from image message without cvbridge
        img = np.frombuffer(msg.data, dtype=np.uint8)
        img = img.reshape((msg.height, msg.width, 3)) 
        # img = img.reshape((msg.height, msg.width, 3))[:,:,::-1]

        
        # crop edges from 640x480 to 480x480
        # if img.shape[0] != 480 or img.shape[1] != 640:
        #     img = cv2.resize((640,480), img)
        # img = img[:,80:560,:]
        
        results = self.model(img, size=640)

        detections = results.tolist()[0].xyxy

        detected_names = []
        detected_objects = []
        
        if len(detections>0):
            for detection in detections:                
                # Convert detection parameters to proper datatypes
                # startx, starty, endx, endy, _, cls = detection.numpy().astype('int')
                startx = int(detection[0])
                starty = int(detection[1])
                endx = int(detection[2])
                endy = int(detection[3])
                cls = int(detection[5])

                conf = float(detection[4])
                
                # Add detection overlay to the image
                cv2.rectangle(img,(startx,starty),(endx,endy),(255,0,0),2)
                # cv2.putText(img,f'{names[cls]}: {conf:.2f}',(startx,starty-10),0,0.5,(255,0,0))
                self.draw_text(img, f'{names[cls]}: {conf:.2f}', pos=(startx,starty-10))
                detection_name = names[cls]
                detected_names.append(detection_name)
                
                # detected_object = DetectedObject(startx, starty, endx, endy, conf, cls, detection_name)
                detected_object = [startx, starty, endx, endy, conf, cls, detection_name]
                detected_objects.append(detected_object)
                

        # total_objects_detected = len(detected_objects)
        # detection_result = DetectionResult(total_objects_detected, detected_objects)
        # detected_obj_names = DetectedObjectNames(total_objects_detected, detected_names)
        
        c = Counter(detected_names)
        # detection_count = DetectionCount(total_objects_detected, c.keys(), c.values())

        # rospy.loginfo(detected_names)
        # rospy.loginfo(detected_objects)
        # rospy.loginfo(dict(c))
        self.detection_names_pub.publish(json.dumps(detected_names))
        self.detection_objects_pub.publish(json.dumps(detected_objects))
        self.detection_counter_pub.publish(json.dumps(dict(c)))
        # self.detection_names_pub.publish(String(','.join(detected_names)))
        # rospy.loginfo(','.join(detected_names))
        
        # rospy.loginfo(','.join(detected_coords))


        img_msg = Image(height=480, width=640, encoding='rgb8', is_bigendian=0, step=1920, data=img.flatten().tobytes())
        self.image_pub.publish(img_msg)

    def __init__(self):
        rospy.init_node('yolov5_object_detector', anonymous=False)

        # If True a service is called for object detection
        as_a_service = rospy.get_param('~as_a_service', False)
        
        # YOLOV5 Parameters
        rospack = rospkg.RosPack()
        ROS_YOLOV5_PATH = rospack.get_path('ros_yolov5')
        YOLO_PATH = rospy.get_param('~yolo_path', os.path.join(ROS_YOLOV5_PATH, 'yolov5'))
        WEIGHTS_PATH = rospy.get_param('~weights_path', os.path.join(ROS_YOLOV5_PATH, 'weights', 'sciroc2021_ep1.pt'))
        
        self.model = torch.hub.load(YOLO_PATH, 'custom', WEIGHTS_PATH, source='local')

        # Detection parameters and publisher definitions
        detection_queue = 1

        detection_image_topic = rospy.get_param('~detection_image_topic', '/object_detection/image')
        self.image_pub = rospy.Publisher(detection_image_topic,
                                         Image,
                                         queue_size=detection_queue)

        detection_counter_topic = rospy.get_param('~detection_counter_topic', '/object_detection/counter')
        self.detection_counter_pub = rospy.Publisher(detection_counter_topic,
                                         String,
                                         queue_size=detection_queue)

        detection_names_topic = rospy.get_param('~detection_names_topic', '/object_detection/names')
        self.detection_names_pub = rospy.Publisher(detection_names_topic,
                                         String,
                                         queue_size=detection_queue)

        detection_objects_topic = rospy.get_param('~detection_objects_topic', '/object_detection/objects')
        self.detection_objects_pub = rospy.Publisher(detection_objects_topic,
                                         String,
                                         queue_size=detection_queue)

        # Parameters for subscription to camera for continuous recognition
        source_topic = rospy.get_param('~source_topic', '/camera/rgb/image_raw')
        source_queue = rospy.get_param('~source_queue', 1)
        # Source image subscriber, buffer size increased from 65KB to 16MB for faster response
        self.image_sub = rospy.Subscriber(source_topic, 
                                          Image, 
                                          callback=self.image_callback, 
                                          queue_size=source_queue,
                                          buff_size=2**24)


        rospy.loginfo(f'Node {rospy.get_name()} initiated')
        rospy.loginfo(f'Started as a service: {as_a_service}')
        rospy.loginfo(f'Yolov5 path: {YOLO_PATH}')
        rospy.loginfo(f'Yolov5 weights path: {WEIGHTS_PATH}')
        rospy.loginfo(f'Source img topic: {source_topic}')
        rospy.loginfo(f'Annotated img topic: {source_topic}')
        rospy.loginfo(f'Detection counter topic: {detection_counter_topic}')
        rospy.loginfo(f'Detection names topic: {detection_names_topic}')
        rospy.loginfo(f'Detection objects topic: {detection_objects_topic}')

        rospy.spin()

if __name__ == '__main__':
    od = ObjectDetector()

        
