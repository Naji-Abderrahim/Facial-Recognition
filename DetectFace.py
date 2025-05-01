from tkinter import messagebox

import cv2 as cv
import face_recognition
import numpy as np

# from tensor.GUI import mainFrame

face_image_encoding = None
face_exist = 0
message = 0


def detectFaceImage(image_path):
    global face_image_encoding
    face = face_recognition.load_image_file(image_path)
    rgb_face = face[:, :, ::-1]
    location = face_recognition.face_locations(rgb_face)
    face_image_encoding = face_recognition.face_encodings(face)
    for (top, right, bottom, left) in location:
        cv.rectangle(face, (left, top), (right, bottom), (255, 0, 0), 2)
    return face


def resetFaceEncoding():
    global face_image_encoding
    face_image_encoding = None


def detectFaceVideo(cap):
    ret, frame = cap.read()
    if cap.isOpened():
        frame, mess, num_faces, sim, nonsim = createRectangle(frame)
        return ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB), mess, num_faces, sim, nonsim
    else:
        return None, None, None, None, None, None


def createRectangle(frame):
    # resize given frame if needed
    # resized_frame = cv.resize(frame, [0, 0], fx=1 / 4, fy=1 / 4)
    # rgb_resized_frame = resized_frame[:, :, ::-1]
    face_localisation = face_recognition.face_locations(frame)
    video_encoding = face_recognition.face_encodings(
            face_image=frame
            )
    frame, mess, sim, nonsim = compareFaces(
            frame,
            face_image_encoding,
            video_encoding,
            face_localisation
            )
    return frame, mess, len(face_localisation), sim, nonsim


def compareFaces(frame, image_encoding, video_encoding, face_locations):
    global face_exist, message, similarfaces, nonsimilarfaces
    try:
        if image_encoding:
            similarfaces, nonsimilarfaces = 0, 0
            for face_video_encoding in video_encoding:
                matches = face_recognition.compare_faces(image_encoding, face_video_encoding)
                face_distances = face_recognition.face_distance(image_encoding, face_video_encoding)
                best_match_index = np.argmin(face_distances)
                for (top, right, bottom, left) in face_locations:
                    if matches[best_match_index]:
                        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                        face_exist += 1
                        similarfaces = len(face_locations)
                    else:
                        cv.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                        face_exist = 0
                        nonsimilarfaces = len(face_locations)
            message = face_exist
        return frame, message, similarfaces, nonsimilarfaces
    except:
        messagebox.showwarning("no image","insert image first!")
        return frame, 31, 0, 0

