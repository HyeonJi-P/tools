import os
import pandas as pd


path = '/home/agtech-research/바탕화면/New_storage/alarad_label_P2'

# 서브 디렉토리 목록 출력
for root, subdirs, files in os.walk(path):

    for d in subdirs:
        fullpath = root + '/' + d
        print(fullpath)

print()
Date = []  # 촬영일
Time = []  # 촬영시
Line = []  # 촬영 라인
View = []  # Topview, sideview
Position = []  # 촬영위치
filename = []  # 파일명
Rootdirs = []  # 추후 파일 찾기 편하려고 만든 루트

D_N = []  # 오전 오후 구분


# 서브 디렉토리별 파일 개수 출력
for root, subdirs, files in os.walk(path):

    if len(files) > 0:
        #cnt = 0;
        for i in files:
            if len(i.split('_')) > 1:
                try:
                    Date.append(i.split('_')[0])
                    Time.append(i.split('_')[1])
                    if int(i.split('_')[1]) > 160000:
                        D_N.append(1)
                    else:
                        D_N.append(0)  # 낮
                    Line.append(i.split('_')[2])
                    View.append(i.split('_')[3])
                    Position.append(i.split('_')[4])
                    filename.append(i)
                    Rootdirs.append(root)

                except:
                    print(i)
        #print(root, len(files),cnt)

myData = {
    'filename': filename, 'Date': Date, 'Time': Time, 'Line': Line, 'View': View, 'Position': Position, 'Rootdirs': Rootdirs, 'isDay': D_N
}
myDF = pd.DataFrame(myData)

myDF.to_excel('../myDF.xlsx')

# 1. 날짜별 파일 갯수 Line별, View 별
cnt_result = myDF.groupby(['Date', 'Line', 'View', 'isDay']).count()
cnt_result.to_excel('../count_result.xlsx')

# 2. line별 이미지 수
line_result = myDF.groupby(['Line', 'View', 'isDay']).count()
line_result.to_excel('../line_result.xlsx')

# 3. 낮밤으로 구분
DN_result = myDF.groupby(['isDay', 'View']).count()
DN_result.to_excel('../DN_result.xlsx')
