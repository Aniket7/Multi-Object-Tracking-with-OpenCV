# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())

# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create, 
	"mosse": cv2.TrackerMOSSE_create
}
 
# initialize OpenCV's multi-object tracker
trackers = cv2.MultiTracker_create()

# if a video path was not supplied, grab the reference to the webcam
if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)
 
# otherwise grab video file
else:
	vs = cv2.VideoCapture(args["video"])

# loop over frames from the video stream
while True:
	# grab the current frame
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame
 
	if frame is None:
		break
 
	frame = imutils.resize(frame, width=600)


	# grab the updated bounding box coordinates
	(success, boxes) = trackers.update(frame)
 
	# loop over the bounding boxes and draw then on the frame
	for box in boxes:
		(x, y, w, h) = [int(v) for v in box]
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	# show the output
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 's' key is selected, we are going to "select" a bounding box to track
	if key == ord("s"):
		# select the bounding box of the object we want to track
		box = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
 
		# create a new object tracker for the bounding box and add it to our multi-object tracker
		tracker = OBJECT_TRACKERS[args["tracker"]]()
		trackers.add(tracker, frame, box)


	# if the `q` key was pressed, break from the loop
	elif key == ord("q"):
		break
 
# if using a webcam, release the pointer
if not args.get("video", False):
	vs.stop()
 
# otherwise, release the file pointer
else:
	vs.release()
 
# close all windows
cv2.destroyAllWindows()
