import cv2
import numpy as np

# ok -
# perfect - 1,2,3,4,5
# chuck 6
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
image = cv2.imread("pictures\\5.png")
image = cv2.resize(image,(900,900))
(h, w) = image.shape[:2]
print(h,w)
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
blob = cv2.dnn.blobFromImage(image,0.007843, (900,900), 127.5)

# pass the blob through the network and obtain the detections and
# predictions
net.setInput(blob)
detections = net.forward()
detected_objects = []

# loop over the detections
for i in np.arange(0, detections.shape[2]):
	# extract the confidence (i.e., probability) associated with
	# the prediction
	confidence = detections[0, 0, i, 2]

	# filter out weak detections by ensuring the `confidence` is
	# greater than the minimum confidence
	if confidence > 0.2 :
		# extract the index of the class label from the
		# `detections`, then compute the (x, y)-coordinates of
		# the bounding box for the object
		idx = int(detections[0, 0, i, 1])
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
		print([startX, startY, endX, endY],",")

		# draw the prediction on the frame
		label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
		detected_objects.append(label)
		cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
		y = startY - 15 if startY - 15 > 15 else startY + 15
		cv2.putText(image, label, (startX, y),	cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

print(detections)
cv2.imwrite("lot1.jpeg", image)