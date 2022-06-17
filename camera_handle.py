from camera import Camera
import cv2
import numpy as np
import drawer
import time
import os

''' Image show '''
def imshow(img, win_name="Window", x_move=0, fullscreen=False):
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(win_name, x_move, 0)
    if fullscreen:
        cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(win_name, img)

def getCurrentTime():
    time_str = time.strftime('%Y%m%d_%H_%M_%S',time.localtime(time.time()))
    return time_str

def checkPath(path):
    '''Check the folder/path to store the scraping results of the specified user.'''
    if not os.path.isdir(path):
        os.makedirs(path)

'''======================================================================='''
'''namespace'''
SIGN = "$> "

image_count = 1
left_image_count = 1
right_image_count = 1

# Creating a dictionary for image saveing
folders = {"Capture":0, "ColorChecker":1, "WhiteBalance":2, "SFRPlus":3,
"Siemens":4, "FenBianLi":5, "Cancel":-1}
suffixes = {"FormattedTime":0, "NumCount":1, "Customized":2, "Cancel":-1}
suffix_mode = list(suffixes.values())[0]
def getSuffix():
    suffix = ""
    if suffix_mode == 1:
        suffix = str(image_count)
    elif suffix_mode == 2:
        suffix = input(SIGN+"Please input a suffix for the images' name: ")
        if suffix == "Cancel" or suffix == "cancel":
            print(SIGN+"Cancel to save current images.")
            return False, ""
    else:
        suffix = getCurrentTime()
    return True, suffix
'''======================================================================='''

class CameraHandle():
    '''This class is used for camera control and image saving'''

    def __init__(self, working_folder, camera_idx=[0,1], image_width=1920, image_height=1080, sharpness=3, backlight=0):
        '''Constructor: Initializing the properties'''
        self.working_folder = working_folder
        self.save_folder = "Capture"
        self.camera = []
        checkPath(self.working_folder + "/" + self.save_folder)
        for idx in range(0, len(camera_idx)):
            # initializing the camera
            self.camera.append(Camera(camera_idx[idx], image_width, image_height, sharpness, backlight))

        print(SIGN+"Start video capture!")
        print(SIGN+"The defalut folder for saving images is 'Capture'.")
        print(SIGN+"The defalut suffix for images' name is a string of FormattedTime.")

    def getFrame(self):
        frames = []
        for idx in range(0, len(self.camera)):
            frame = self.camera[idx].getFrame()
            frames.append(frame)
            
        return frames


    def showStereoFrame(self, mode=0, win_width=1920, win_height=1080, draw_prompt=False, fov=0, p_of_fov=0):
        '''Displaying the stereo-camera frame streaming.
    
            @param mode The displaying mode, the valid value is following.
                        0 --- displaying both left and right camera frame in a same screen simultaneously.
                        1 --- fullscreen displaying both left and right camera frame in second screen on the right of main screen.
            
            @param draw_prompt Draw some prompt in the images.

            @param fov The field of view of the camera.

            @param proportion_of_fov The proportion of fov for determining the position of the circle in diagnal line.
        '''
        frames = self.getFrame()
        sframes = []
        if draw_prompt:
            for i in range(0,2):
                sframes.append(frames[i].copy())
                # sframes[i] = drawer.drawCenterLine(sframes[i])
                sframes[i] = drawer.drawDiagnalCircle(sframes[i], fov, p_of_fov)
                sframes[i] = drawer.drawDiagnalLine(sframes[i])
                # sframes[i] = drawer.drawLineInWidth(sframes[i])
        else:
            sframes = frames

        if mode == 0:
            scale = 2
            ssFrame1 = cv2.resize(sframes[0], (int(win_width / scale), int(win_height / scale)))
            ssFrame2 = cv2.resize(sframes[1], (int(win_width / scale), int(win_height / scale)))
            cFrame = np.concatenate((ssFrame1, ssFrame2), axis = 1)
            str_win = "Image Window"
            imshow(cFrame, str_win)
            #imshow(cFrame,str_win, 0, True)
        elif mode == 1:
            # show left image
            left_win_name = "capture left"
            imshow(sframes[0], left_win_name, 1*win_width, True)
            # show right image
            right_win_name = "capture right"
            imshow(sframes[1], right_win_name, 1*win_width, True)
        key = cv2.waitKey(5)

        return self.operateKey(key=key, frames=frames)


    def release(self):
        for idx in range(0, len(self.camera)):
            # release the VideoCapture object in each Camera class
            self.camera[idx].release()
        # destroy all the image showing windows
        cv2.destroyAllWindows()

    
    def operateKey(self, key, frames):
        prompt_msg = ""
        frame1 = frames[0]
        frame2 = frames[1]

        path = self.working_folder + "/" + self.save_folder
        img_fmt = '.bmp'

        global suffix_mode
        if key & 0xFF == ord('C'):
            msg = input(SIGN+"Changing image folder(F) or Change suffix select(S) or Cancel(C): ")
            if msg == 'F' or msg == 'f':
                folder_str = ""
                for name, val in folders.items():
                    folder_str += '    '+name+'('+str(val)+')'
                print(folder_str)
                print(SIGN+"Current saving folder is '" + self.save_folder + "'.")
                while(True):
                    select = input(SIGN+"Please select a new folder for saving captured images: ")
                    if int(select) == -1:
                        print(SIGN+"Cancel to change current saving folder.")
                        break
                    elif int(select) in folders.values():
                        self.save_folder = list(folders.keys())[int(select)]
                        print(SIGN+"Current saving folder has been changed to '" + self.save_folder +"'.")
                        # check the path
                        path = self.working_folder + "/" + self.save_folder
                        checkPath(path)
                        break
                    else:
                        print(SIGN+"Wrong selection.")
            elif msg == 'S' or msg == 's':
                suffix_str = ""
                for name,val in suffixes.items():
                    suffix_str += '    '+name+'('+str(val)+')'
                print(suffix_str)
                print(SIGN+"Current suffix mode is set as '" + list(suffixes.keys())[suffix_mode] + "'.")
                while(True):
                    # select whether need to add suffix when saving image
                    select = input(SIGN+"Please select a new suffix mode for saving captured images' name: ")
                    if int(select) == -1:
                        print(SIGN+"Cancel to change current suffix mode.")
                        break
                    elif int(select) in suffixes.values():
                        suffix_mode = int(select)
                        print(SIGN+"Current suffix mode has been changed to '" + list(suffixes.keys())[suffix_mode],"'.")
                        break
                    else:
                        print(SIGN+"Wrong selection.")
                        break
            print(SIGN+"Changing done!")
            return True

        elif key & 0xFF == ord('q') or key & 0xFF == ord('Q') or key & 0xFF == 27: # Esc
            print(SIGN+"Quitting!\n") # Stop the thread
            return False

        elif key & 0xFF == 32:  # Space
            print(SIGN+"Capturing images...")
            ret, suffix = getSuffix()
            if not ret:
                return True
            cv2.imwrite(path + '/L_' + suffix + img_fmt, frame1)
            cv2.imwrite(path + '/R_' + suffix + img_fmt, frame2)
            prompt_msg = "Both left and right " + self.save_folder +" images with name suffix ["+ suffix + "] saved."

        elif key & 0xFF == ord("L") or key & 0xFF == ord("l"):
            ret, suffix = getSuffix()
            if not ret:
                return True
            cv2.imwrite(path + '/L_' + suffix + img_fmt, frame1)
            prompt_msg = "Left " + self.save_folder +" image with name suffix ["+ suffix + "] saved."

        elif key & 0xFF == ord("R") or key & 0xFF == ord("r"):
            ret, suffix = getSuffix()
            if not ret:
                return True
            cv2.imwrite(path + '/R_' + suffix + img_fmt, frame2)
            prompt_msg = "Right " + self.save_folder +" image with name suffix ["+ suffix + "] saved."

        elif key & 0xFF == ord('P') or key & 0xFF == ord('p'):
            print(SIGN+'Prompting of valid key operation:')
            print("\t'Space bar' used for capturing two stereo images.")
            print("\t'L/l' used for capturing left image.")
            print("\t'R/r' used for capturing right image.")
            print("\t'C' used for changing the folder for saving images.")
            print("\t'Q/q' used for quiting.")
        else:
            return True

        print(SIGN+prompt_msg)
        return True