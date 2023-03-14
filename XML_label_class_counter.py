import numpy as np
import pandas as pd
import json
import os
import xml.etree.ElementTree as ET
import shutil


################################################################################################################
#수정 필요한 부분 (xml파일위치, 라벨 종류)
xml_path="-" ########################
img_path = "-"
save_path ='-'
label_names = []
#label_color = [(255,204,204),(204,153,255),(255,204,0),(255,153,51),(51,255,204),(0,102,204),(255,0,0)]
#################################################################################################################
File_path=[]
File_names=[]
N_flower=[]
N_fold_flower=[]
N_receptacle=[]
N_greenSF=[]
N_str1=[]
N_str2=[]
N_str3=[]

def tw_bbox_class_counter(img_dir):
    fname=[]
  
    fname.append(xml_path) #여러개 한번에 할 경우 xml file append
  
    for i in range(len(fname)):
        anno_doc = ET.parse(fname[i])
        annoD_root = anno_doc.getroot()
        for items in annoD_root.iter("image")   :
            filename = items.attrib["name"]
            
            boxlist = items.findall("box")
            
            record={}
            record["file_name"] = img_dir+filename
            
            File_path.append(img_dir+filename)
            File_names.append(filename)
            N_flower.append(0)
            N_fold_flower.append(0)
            N_receptacle.append(0)
            N_greenSF.append(0)
            N_str1.append(0)
            N_str2.append(0)
            N_str3.append(0)

            
            for bidx in range(len(boxlist)): 
                #xml에서 박스 찾기 및 저장된 속성값 가져오기
                
                
                box_class = boxlist[bidx].attrib["label"]
                cateid=0
                

                for label_idx in range(0,len(label_names)):
                    
                    if box_class == label_names[label_idx]:
                        cateid = label_idx

                        if label_idx == 0:
                            N_flower[-1] +=1

                        elif label_idx == 1:
                            N_fold_flower[-1] +=1

                        elif label_idx == 2:
                            N_receptacle[-1] +=1

                        elif label_idx == 3:
                            N_greenSF[-1] +=1

                        elif label_idx == 4:
                            N_str1[-1] +=1

                        elif label_idx == 5:
                            N_str2[-1] +=1

                        elif label_idx == 6:
                            N_str3[-1] +=1
                        

    print("len filename:",len(File_names))
    print("len str1: ",len(N_str1))

tw_bbox_class_counter(img_path)

myData = {
    'filename': File_names, 'flowers': N_flower, 'before_blooming': N_fold_flower, 'receptacle':N_receptacle, 'green_small_fruit':N_greenSF, 'strawberry1':N_str1, 'strawberry2':N_str2, 'strawberry3':N_str3, 'file_path':File_path
}

myDF=pd.DataFrame(myData)
myDF.to_excel('./label_class_count.xlsx')