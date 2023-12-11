from PIL import Image, ImageEnhance
import cv2
import numpy as np
import os
import numpy as np
def darken_highlights(image_path, output_image_path, decrease_percent):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv)
    v = np.where(v <= 160, v, v * decrease_percent * 0.4).astype(np.uint8)
    v = np.where(v <= 127, v, v * decrease_percent * 0.9).astype(np.uint8)
    v = np.where(v <= 100, v, v * decrease_percent).astype(np.uint8)
    s= np.uint8(s*0.8)
    final_hsv = cv2.merge([h, s, v])

    dark_img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    fog = cv2.imread('fog_mask.png',cv2.IMREAD_UNCHANGED)
    alpha = fog[:,:,3]
    alpha = cv2.cvtColor(alpha,cv2.COLOR_GRAY2BGR)
    alpha = alpha.astype(float)/255

    fore = fog[:,:,0:3].astype(float)
    # Multiply the foreground with the alpha matte
    foreground = cv2.multiply(alpha, fore)
    dark_img = dark_img.astype(float)
    # Multiply the background with ( 1 - alpha )

    background = cv2.multiply(1.0 - alpha, dark_img)
    
    # Add the masked foreground and background.
    outImage = cv2.add(foreground, background)
    cv2.imwrite(output_image_path, outImage)
for i in range(1,1100):
    os.rename("calib/" + str(i).zfill(6) + ".txt", "calib/" + str(i+10000).zfill(6) + ".txt")
# for i in range(1,1100):
#     source_path = "/home/jheidegg/kitti_data/training/image_2/" + str(i).zfill(6) + ".png"
#     dest_path = "image_mod/" + str(i + 10000).zfill(6) + ".png"
#     darken_highlights(source_path, dest_path, 0.75)
#     os.rename("label_2/" + str(i).zfill(6) + ".txt", "label_2/" + str(i+10000).zfill(6) + ".txt")