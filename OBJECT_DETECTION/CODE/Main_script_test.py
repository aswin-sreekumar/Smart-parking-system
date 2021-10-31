import cv2
import OBJECT_DETECTION.CODE.util_new as detect_utils
from OBJECT_DETECTION.CODE import Bounding_Box as bbox_list
import os
directory = os.getcwd()
city_encode = {"chn":"chennai"}
print(directory)
print(os.listdir())

# espxx_chn_1_time

park = detect_utils.parking_slot_management("chennai", "chn2", "C:\\Users\\grees\\PycharmProjects\\parklot\\final\\NEW-PICS\\3.jpeg" )

# detect outputs
boxes, classes = park.predict_cv()
# print(boxes)

# updation of slots
park.updation_of_slots(boxes, classes)

# just draw boxex
# park.draw_boxes(bbox_list.chn4, classes)

# print(len(park.comp))
# check availability of parking slots
park.find_park_slot()

cv2.imwrite("C:\\Users\\grees\\PycharmProjects\\parklot\\final\\NEW-PICS\\check.jpeg",park.image)


#
# while(True):
#     for i in os.listdir():
#         val = i.split("_")
#         if ".jpeg" in i and len(val) > 1:
#             print(val)
#             city = city_encode[val[1]]
#             slot_id = val[1]+val[2]
#             print(city,slot_id)
#
#             park = detect_utils.parking_slot_management(city,slot_id,i)
#
#             # detect outputs
#             boxes, classes = park.predict_cv()
#             # print(boxes)
#
#             # updation of slots
#             # park.updation_of_slots(boxes, classes)
#
#             # just draw boxex
#             park.draw_boxes(boxes,classes)
#
#             # print(len(park.comp))
#             # check availability of parking slots
#             park.find_park_slot()
#             # deleting image
#             os.remove(i)
#
#
#
#
#
#
#
