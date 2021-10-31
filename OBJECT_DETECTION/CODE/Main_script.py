import cv2
import OBJECT_DETECTION.CODE.util_new as detect_utils
import os

directory = os.getcwd()
city_encode = {"chn":"chennai"}

# espxx_chn_1_time.jpeg



while(True):
    for i in os.listdir():
        val = i.split("_")
        if ".jpeg" in i and len(val) == 4:
            # print(val)
            city = city_encode[val[1]]
            slot_id = val[1]+val[2]
            date = val[3].rstrip(".jpeg")
            print("-------------------------------------------------------------")
            print("image name -- ",i)
            print("Updating slotno. -- ",slot_id,"City -- ",city,"Date -- ",date)

            park = detect_utils.parking_slot_management(city,slot_id,i)

            # detect outputs
            boxes, classes = park.predict_cv()
            # print(boxes)

            # updation of slots
            park.updation_of_slots(boxes, classes)

            # saving image
            img_name= "OCCUPANCY-"+val[0]+"-"+slot_id+"-"+date+".png"
            img_name = "C:\\Users\\grees\\PycharmProjects\\parklot\\final\\UPDATED_SLOTS_IMAGES\\"+img_name

            cv2.imwrite(img_name, park.image)
            # deleting image
            os.remove(i)







