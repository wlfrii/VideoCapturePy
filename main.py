from camera_handle import CameraHandle
import math
import sys

'''================= Preset ================='''
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
SHARPNESS = 3
BACKLIGHT = 0

P_of_FOV = 0.9

WIN_WIDTH = 1920
WIN_HEIGHT = 1080

working_folder = "./Capture"
version = 1.2
# working_folder = "E:/Rii/20200106-20200813_Endoscope_Image/Color_Correction"
'''=========================================='''

def getCamIdx(siwtch=0):
    if siwtch == 0:
        cam_id = [1,0]
    elif siwtch == 1:
        cam_id = [0,1]
    else:
        cam_id = [2,3]
    return cam_id

def run(argv=[]):
    try:
        FOV = float(argv[1])
    except:
        FOV = 90
    try:
        if(int(argv[2]) == 0):
            is_draw_prompt = False
        else:
            is_draw_prompt = True
    except:
        is_draw_prompt = True
    try:
        if(int(argv[3]) == 0):
            is_cam_opposite = 0
        else:
            is_cam_opposite = 1
    except:
        is_cam_opposite = 0

    info = "***********************************************************************\n\n" \
        + "                         Stereo Camera Capture                          \n\n" \
        + "Version: " + str(version) + "\n\n" \
        + "Author: Wanglf\n\n" \
        + "Guidance:\n" \
        + "\tFocus the view on the camera display window, and press 'P' or 'p'\n" \
        + "you will see the propmtion of this application.\n" \
        + "\tFor exit the application, press 'Q' or 'q'.\n\n" \
        + "The inputs of the application are the followings.\n\n" \
        + "\targv[]=[FOV=90, draw_propmt=0/1, camera_opposite=0/1]\n\n" \
        + "FOV denotes the Field of View, default value is 90 degree; draw_propmt\n" \
        + "will decide whether drap the prompts, defalut is True; camera_opposite\n" \
        + "decide whether the displayed cameras are opposited, default is False. \n" \
        + "So 0 indicates False, 1 indicates True\n\n" \
        + "If you want to set the input [argv], you should run this application\n" \
        + "in the Windows command line, and with the command like: \n\n" \
        + "C:/Users/XXX/Desktop>./Capture.exe 90 1 0\n\n"
    print(info)
    print("Current argv: Fov=%f, draw_prompt=%d, camera_opposite=%d" % (FOV, is_draw_prompt, is_cam_opposite))
    print("***********************************************************************")
    cam_hd = CameraHandle(working_folder=working_folder, camera_idx=getCamIdx(is_cam_opposite), image_width=IMAGE_WIDTH, image_height=IMAGE_HEIGHT)
    while(True):
        ret = cam_hd.showStereoFrame(draw_prompt=is_draw_prompt, fov=FOV/180.0*math.pi, p_of_fov=P_of_FOV)
        if not ret:
            break
    cam_hd.release()

if __name__ == "__main__":
    run(sys.argv)