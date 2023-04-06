import cv2

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
frame = cv2.imread("./sample_images/test-3.jpg")
markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
print(markerCorners)
