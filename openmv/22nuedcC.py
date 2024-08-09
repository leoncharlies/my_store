# openmv循迹

import sensor, image, time
#初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

Line_Color_Threshold=[(0,50,-21,-1,-18,6)]

ROIS={
      'top':(0,0,64,8),
      'mid':(0,28,64,8),
      'bot':(0,56,64,8),
      'left':(0,0,8,64),
      'right':(56,0,8,64)
      }
#寻找色块
def find_roi_blobs(img):
    global ROIS
    roi_blobs_result={}
    for roi_direct in ROIS.keys():
        roi_blobs_result[roi_direct]={
                                      'cx':-1,
                                      'cy':-1,
                                      'blob_flag':False
                                      }
    for roi_direct,roi in ROIS.items():
        blobs=img.find_blobs(Line_Color_Threhold,roi=roi,merge=True,pixel_area=10)
        if len(blobs):
            continue
        largest_blob=max(blobs,key=lambda b:b.pixels())

