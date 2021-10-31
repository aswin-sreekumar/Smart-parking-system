import cv2
import numpy as np
from pymongo import MongoClient
from OBJECT_DETECTION.CODE import Bounding_Box as bbox_list

# self.input_img = "D:\\IIT_M\\Parking-Lot.jpg"
class parking_slot_management():
    def __init__(self,CITY,SLOTID,PATH):
        self.net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
        self.client = MongoClient("mongodb+srv://ip-module:smartcity2021@romainparkingdb.ua9uf.mongodb.net/parking-slots?retryWrites=true&w=majority")
        self.city = CITY
        self.slotid = SLOTID
        self.total_slots = bbox_list.total_slots[self.slotid]
        self.input_img = PATH
        self.image = cv2.imread(self.input_img)
        self.image = cv2.resize(self.image, (900, 900))
        # load our serialized model from disk
        # print("[INFO] loading model...")


        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        # slots bounding box
        self.comp = bbox_list.slot_id[self.slotid]

        self.parking_slots_id = {}
        self.parking_slots_occupancy = {}
        for i in range(len(self.comp)):
            self.parking_slots_id[tuple(self.comp[i])] = i + 1
            self.parking_slots_occupancy[i+1] = 0

    def predict_cv(self):
        (h, w) = self.image.shape[:2]
        # print(h, w)
        COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        blob = cv2.dnn.blobFromImage(self.image,0.007843, (h,w), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        self.net.setInput(blob)
        detections = self.net.forward()
        detected_objects = []
        bounding_box = []

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]
            idx = int(detections[0, 0, i, 1])

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.2 and (self.CLASSES[idx] == "car"or self.CLASSES[idx] == "bus" or self.CLASSES[idx] == "motorbike"):
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                # print([startX, startY, endX, endY],",")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                detected_objects.append(label)
                bounding_box.append([startX, startY, endX, endY])
                # cv2.rectangle(self.image, (startX, startY), (endX, endY), (0,255,0), 2)

                # y = startY - 15 if startY - 15 > 15 else startY + 15
                # cv2.putText(self.image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        # print(detections)
        # cv2.imwrite("Parking-Lot.jpg", self.image)
        (h, w) = self.image.shape[:2]
        # print(h, w)
        return bounding_box, detected_objects


    def update_DB(self,count):
        db = self.client.get_database('parking-slots')
        collection = db.get_collection(self.city.lower())
        collection.find_one_and_update({'slotid': self.slotid}, {'$set': {'filledslots': count,'totalslots':self.total_slots}})
        # print(city_['lots'])



    def reseting_slots(self):

        self.image = cv2.imread(self.input_img)
        self.update_DB(0)
        for i,corresponding_box in enumerate(self.comp):
            self.parking_slots_occupancy[i+1] = 0
            cv2.rectangle(self.image, (int(corresponding_box[0]), int(corresponding_box[1])), (int(corresponding_box[2]), int(corresponding_box[3])), (0, 0,255), 2)
            # cv2.putText(self.image, "Unoccupied", (int(corresponding_box[0]), int(corresponding_box[1] - 5)),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0,255), 2, lineType=cv2.LINE_AA)


    def IOU(self,boxA, boxB):
        # determine the (x, y)-coordinates of the intersection rectangle
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        # compute the area of intersection rectangle
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
        # compute the area of both the prediction and ground-truth
        # rectangles
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = interArea / float(boxAArea + boxBArea - interArea)
        # return the intersection over union value
        return iou

    def draw_boxes(self, boxes,classes):
        self.image = cv2.cvtColor(np.asarray(self.image), cv2.COLOR_BGR2RGB)
        for i, box in enumerate(boxes):
                color = (0, 0, 255)
                cv2.rectangle(self.image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), color, 2)
                # cv2.putText(self.image, classes[i], (int(box[0]), int(box[1] - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                #             color, 2,
                #             lineType=cv2.LINE_AA)



    def updation_of_slots(self,boxes,classes):
        # reset all slots to unoccupied then update
        self.reseting_slots()
        occupied_count = 0
        for i, box in enumerate(boxes):
            # # to find relevent boxes
            # if classes[i] == "car":
            box_with_max_iou = 0
            corresponding_box = []
            for box1 in self.comp:
                iou = self.IOU(box1, box)
                if (box_with_max_iou < iou):
                    # print(iou)
                    box_with_max_iou = iou
                    # finding box with maximum iou
                    corresponding_box = box1

            if len(corresponding_box) != 0 and box_with_max_iou > 0.9:
                # print(box_with_max_iou)
                # making it occupied
                # print(tuple(corresponding_box))
                self.parking_slots_occupancy[self.parking_slots_id[tuple(corresponding_box)]] = 1
                # drawing bounding box
                cv2.rectangle(self.image, (int(corresponding_box[0]), int(corresponding_box[1])), (int(corresponding_box[2]), int(corresponding_box[3])), (0,255,0), 2)
                # cv2.putText(self.image, "Occupied", (int(corresponding_box[0]), int(corresponding_box[1] - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2,lineType=cv2.LINE_AA)
                occupied_count+=1
        # print(occupied_count)
        # print()
        # to update in site
        self.update_DB(occupied_count)
        print("occupance updated to", occupied_count, "out of", self.total_slots)




    def find_park_slot(self):
        for i in self.parking_slots_occupancy:
            if self.parking_slots_occupancy[i] == 0:
                print("slot",i," is unoccupied")
                return
        print("all slots occupied")











