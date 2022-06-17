# VideoCapturePy

A useful tiny tool for capture images.

## Requirements

+ Python
+ OpenCV

## Introduction

These files were created two years ago, aimed at easily capturing USB stereo camera image. And now, these codes are arranged to be open.

There are Three optional input arguments can be given when starting the app. The details of the input arguments can be found in [main.py](https://github.com/wlfrii/VideoCapturePy/blob/main/main.py). Three inputs are:
 + __FOV__ - Default field of view is set to __87 degrees__;
 + __0/1__ - Flag for whether draw prompt line. (The green lines denote the dignal line, while the yellow circles denote the position with __90% FOV__);
 + __0/1__ - Flag for whether need to change left and right image position, which is considered when the left and right image is oppsite.


The default folder to store the captured image is set to `./Capture`, a relative path to the application. And the folders to store different kinds of images, such as __ColorChecker__, __SFR__, __WhilteBalance__, _et.al_, can be specified during capturing. The default name of the captured image is set to timestamp. The users could also specify the captured name when saving image.

Some useful keys and its corresponding functions:
 + __Space__ - Do capture
 + __q__     - Exit application
 + __p__     - Show prompts