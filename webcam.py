# from utils import *
#
# # # by Webcam
# video_capture = cv2.VideoCapture(0)
# while True:
#     ret_val, frame = video_capture.read()
#     frame = cv2.flip(frame, 1)
#     if ret_val:
#         cv2.imshow("Original", frame)
#         feat_applied = apply_makeup(frame, True, 'lips', False)
#         cv2.imshow("Feature", feat_applied)
#
#         if cv2.waitKey(1) == 27:
#             break
