import os, shutil
import pandas as pd


#path = '/home/hyeonji/detectron2/label_checker_testworksXML/TW_strawberry_output/dataset_pool/'

# 엑셀 파일을 읽어와 dataframe으로 변환
myDF = pd.read_excel('/home/hyeonji/detectron2/label_checker_testworksXML/TW_strawberry_output/dataset_pool/7class_500_datasplit_info.xlsx')

# TVT열의 값을 확인하여 파일을 복사할 디렉토리 결정
for index, row in myDF.iterrows():
    tvt_value = row['TVTs']
    file_name = row['filename']
    
    labelname = file_name.split('.')
    labelname = labelname[0]+'.txt'
    if tvt_value == 0:
        shutil.copy("./img_pool/"+file_name, './img_pool/train/'+file_name)
        shutil.copy("./label_pool/"+labelname, './label_pool/train/'+labelname)

    elif tvt_value == 1:
        shutil.copy("./img_pool/"+file_name, './img_pool/val/'+file_name)
        shutil.copy("./label_pool/"+labelname, './label_pool/val/'+labelname)

    elif tvt_value == 2:
        shutil.copy("./img_pool/"+file_name, './img_pool/test/'+file_name)
        shutil.copy("./label_pool/"+labelname, './label_pool/test/'+labelname)

    else:
        print('Invalid TVTs value:', tvt_value)