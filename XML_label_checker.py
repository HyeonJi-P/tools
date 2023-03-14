import numpy as np
import os, json, cv2, random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import json
import os

import xml.etree.ElementTree as ET
import shutil


################################################################################################################
#수정 필요한 부분 (xml파일위치, 라벨 종류)
xml_path="" ########################
img_path = ""
save_path =''
label_names = []
label_color = [(255,204,204),(204,153,255),(255,204,0),(255,153,51),(51,255,204),(0,102,204),(255,0,0)]
#################################################################################################################


def tw_bbox_visualize(img_dir):
    fname=[]
  
    fname.append(xml_path) #여러개 한번에 할 경우 xml file append
  
    for i in range(len(fname)):
        anno_doc = ET.parse(fname[i])
        annoD_root = anno_doc.getroot()
        for items in annoD_root.iter("image")   :
            filename = items.attrib["name"]
            
            boxlist = items.findall("box")
            
            record={}
            record["file_name"] = img_dir+"/"+filename
            record["image_id"] = items.attrib["id"]
            record["height"] = int(items.attrib["height"])
            record["width"] = int(items.attrib["width"])

            #print(boxlist)
            
            objs = []
            for bidx in range(len(boxlist)): 
                #xml에서 박스 찾기 및 저장된 속성값 가져오기
                #occ = boxlist[bidx].attrib["occluded"] #사용은 안함
                
                box_class = boxlist[bidx].attrib["label"]
                cateid=0
                for label_idx in range(0,len(label_names)):
                    if box_class == label_names[label_idx]:
                      cateid = label_idx

                xmax= boxlist[bidx].attrib["xbr"]
                xmin= boxlist[bidx].attrib["xtl"]
                ymax= boxlist[bidx].attrib["ybr"]
                ymin= boxlist[bidx].attrib["ytl"]    
                z_number= boxlist[bidx].attrib["z_order"]

                px = [float(xmax), float(xmin)]
                py = [float(ymax), float(ymin)]   



                obj = {
                    "bbox": [np.min(px), np.min(py), np.max(px), np.max(py)],
                    #"bbox_mode": BoxMode.XYXY_ABS,
                    #"segmentation": [],
                    "category_id": cateid,
                    "bbox_number": z_number,
                }
                objs.append(obj)

            img1 = Image.open(record["file_name"])
            draw = ImageDraw.Draw(img1)
            for nAnno in range(len(boxlist)):
              map_box = objs [nAnno]
              
              #print(map_box)
              print("=>",map_box['bbox'], "=>",map_box['category_id'])
              
              # label명 표기
              draw.text((map_box['bbox'][0]+5,map_box['bbox'][1]),label_names[map_box['category_id']],(200,200,200))
              # bbox 검수를 위한 번호표기
              draw.text((map_box['bbox'][0]+5,map_box['bbox'][1]-10),map_box['bbox_number'],(45,250,255))
              #bbox그리기
              draw.rectangle((map_box['bbox'][0],map_box['bbox'][1], map_box['bbox'][2],map_box['bbox'][3]), outline=label_color[map_box['category_id']], width = 3) 

            img1.save(save_path+filename.split('.')[0]+'.jpg') #저장


tw_bbox_visualize(img_path)