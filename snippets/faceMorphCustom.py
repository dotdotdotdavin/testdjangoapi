# Copyright 2017 BIG VISION LLC ALL RIGHTS RESERVED
#
# This code is made available to the students of
# the online course titled "Computer Vision for Faces"
# by Satya Mallick for personal non-commercial use.
#
# Sharing this code is strictly prohibited without written
# permission from Big Vision LLC.
#
# For licensing and other inquiries, please email
# spmallick@bigvisionllc.com
#
import sys
import cv2
import dlib
import numpy as np
from . import faceBlendCommonCustom as fbc
import imageio
import os
import urllib.request as url_req
import ssl
import datetime

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
  context1 = ssl._create_unverified_context()
  resp = url_req.urlopen(url, context=context1)
  image = np.asarray(bytearray(resp.read()), dtype="uint8")
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)
  return image

def faceMorph(url1,url2):
    # Landmark model location
  temp_path = os.path.dirname(os.path.abspath(__file__))
  PREDICTOR_PATH = temp_path+"/shape_predictor_68_face_landmarks.dat"

  # Get the face detector
  faceDetector = dlib.get_frontal_face_detector()
  # The landmark detector is implemented in the shape_predictor class
  landmarkDetector = dlib.shape_predictor(PREDICTOR_PATH)

  # Read two images
  # im1 = cv2.imread("../data/images/jeon.jpg")
  # im2 = cv2.imread("../data/images/soohee.jpg")
  im1 = url_to_image(url1)
  im2 = url_to_image(url2)

  # Detect landmarks in both images.
  points1 = fbc.getLandmarks(faceDetector, landmarkDetector, cv2.cvtColor(im1, cv2.COLOR_BGR2RGB))
  points2 = fbc.getLandmarks(faceDetector, landmarkDetector, cv2.cvtColor(im2, cv2.COLOR_BGR2RGB))

  points1 = np.array(points1)
  points2 = np.array(points2)

  # Convert image to floating point in the range 0 to 1
  im1 = np.float32(im1)/255.0
  im2 = np.float32(im2)/255.0

  # Dimensions of output image
  h = 600
  w = 600

  # Normalize image to output coordinates.
  imNorm1, points1 = fbc.normalizeImagesAndLandmarks((h, w), im1, points1)
  imNorm2, points2 = fbc.normalizeImagesAndLandmarks((h, w), im2, points2)

  # Calculate average points. Will be used for Delaunay triangulation.
  pointsAvg = (points1 + points2)/2.0

  # 8 Boundary points for Delaunay Triangulation
  boundaryPoints = fbc.getEightBoundaryPoints(h, w)
  points1 = np.concatenate((points1, boundaryPoints), axis=0)
  points2 = np.concatenate((points2, boundaryPoints), axis=0)
  pointsAvg = np.concatenate((pointsAvg, boundaryPoints), axis=0)

  # Calculate Delaunay triangulation.
  rect = (0, 0, w, h)
  dt = fbc.calculateDelaunayTriangles(rect, pointsAvg)

  # Start animation.
  alpha = 0
  increaseAlpha = True

  namesArr = []
  imagesArr =[]

  while alpha <= 1.025:
    # Compute landmark points based on morphing parameter alpha
    pointsMorph = (1 - alpha) * points1 + alpha * points2

    # Warp images such that normalized points line up with morphed points.
    imOut1 = fbc.warpImage(imNorm1, points1, pointsMorph.tolist(), dt)
    imOut2 = fbc.warpImage(imNorm2, points2, pointsMorph.tolist(), dt)

    # Blend warped images based on morphing parameter alpha
    imMorph = (1 - alpha) * imOut1 + alpha * imOut2

    # Keep animating by ensuring alpha stays between 0 and 1.
    # if (alpha <= 0 and not increaseAlpha):
    #   increaseAlpha = True
    # if (alpha >= 1 and increaseAlpha):
    #   increaseAlpha = False

    b = str(alpha)
    b = b[0:5]
    if b == "0":
      b = "0-000"
    b = b.replace(".","-")

    b1 = "media/images/"+b+".jpg"

    # cv2.imshow("Morphed Face", imMorph)
    imM2 = imMorph *255
    imM2 = np.uint8(imM2)
    
    cv2.imwrite(b1,imM2)

    namesArr.append(b1)
    imagesArr.append(imageio.imread(b1))

    if increaseAlpha:
      alpha += 0.025
    else:
      alpha -= 0.025


    key = cv2.waitKey(15) & 0xFF

    # Stop the program.
    # if key==27:  # ESC
      # If ESC is pressed, exit.
      # break
  kargs = {'duration':0.1}  
  temp_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  temp_name = 'media/result/result-'+temp_str+'.gif'
  imageio.mimsave(temp_name, imagesArr,'GIF',**kargs)

  for i in namesArr:
    os.remove(i)
  
  return temp_name

