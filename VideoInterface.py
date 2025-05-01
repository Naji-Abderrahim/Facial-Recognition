import cv2 as cv
import subprocess

width_var = None


def getCameraLinux():
    v = cv.VideoCapture(0)
    video_capture_interfaces = v.getBackendName()
    return video_capture_interfaces, 0


def getCameraWin():
    import wmi
    c = wmi.WMI()
    wql = "Select * From win32_usbControllerDevice"
    cameras = []
    for item in c.query(wql):
        a = item.Dependent.PNPClass
        b = item.Dependent.Name.upper()
        if (a is not None) and (a.upper() == 'MEDIA' or a.upper() == 'CAMERA') and 'AUDIO' not in b:
            cameras.append(item.Dependent.Name)
    return cameras


def calculSize(init_width, init_height, element_type):
    global width_var
    if element_type == 'video':
        width_var = 461
    if element_type == 'image':
        width_var = 360
    height_percent = (270 / init_height)
    width_percent = (width_var / init_width)
    comp_1 = min(width_percent, height_percent)
    if comp_1 < 1:
        if init_width >= init_height and init_width > width_var:
            final_width = init_width - (init_width - width_var)
            if (init_width - width_var) > init_height or (init_width - init_width * 0.25) > init_height:
                if init_height > 270:
                    final_height = init_height - (init_height - 270)
                else:
                    final_height = init_height
            else:
                final_height = init_height - (init_width - width_var)
        else:
            final_height = init_height - (init_height - 270)
            if (init_height - 270) > init_width or (init_height - init_height * 0.25) > init_width:
                if init_width > width_var:
                    final_width = init_width - (init_width - width_var)
                else:
                    final_width = init_width
            else:
                final_width = init_width - (init_height - 270)
        return [final_width, final_height]
    else:
        return [init_width, init_height]


def writeInfoOverTime(cap):
    fps = cap.get(cv.CAP_PROP_FPS)
    frame_c = cap.get(cv.CAP_PROP_FRAME_COUNT)
    duration = float((frame_c / fps))
    return duration
