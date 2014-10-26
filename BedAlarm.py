import cv2
import numpy as np
import pygame

pygame.init()

pygame.mixer.music.load("./alarms/getout.mp3")

print cv2.__version__

cap = cv2.VideoCapture(0)
cv2.namedWindow('bg')
kernel = np.ones((2,2),np.uint8)
fgbg = cv2.createBackgroundSubtractorMOG2()

def mouseCallback(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		print opening[y,x]

cv2.setMouseCallback('bg',mouseCallback)

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	fgmask = fgbg.apply(frame)
	opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
	opening = cv2.dilate(opening,kernel,iterations = 1)
	_, thresh = cv2.threshold(opening, 50, 255, cv2.THRESH_BINARY)

	_, contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	max_area = 0
	for contour in contours:
		M = cv2.moments(contour)
		try:
			centroid_x = int(M['m10']/M['m00'])
			centroid_y = int(M['m01']/M['m00'])
			area = cv2.contourArea(contour)
			if area>max_area:
				max_area = area
			cv2.circle(frame,(centroid_x,centroid_y), int(area), (0,0,255))
		except:
			pass

	if max_area>2000:
		print "detection"		
		pygame.mixer.music.play()

	cv2.imshow('bg',opening)
	print max_area
	# Display the resulting frame
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()