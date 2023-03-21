import os, shutil
import pandas as pd
import numpy as np

"""
좋은 이미지 선별을 위한 규칙
    1. 목표지점(베드)의 화질이 선명할 것 
    2. 이미지내 객체가 충분할 것
    3. 딸기 식물체가 가능한 반절 이상 존재할 것
    4. 객체가 너무 난잡하게 겹쳐있지는 않을 것

제외 필요한 부분
    1. 끝라인: Position 01, 02, 30
                + L3의 02 03

추후 직접 확인해야하는 부분
    1. L3 P22-28
    2. L1 P..
"""

def sort_analyze_df (myDFs):
    # 1. 날짜별 파일 갯수 Line별, View 별
    cnt_result = myDFs.groupby(['Date', 'Line', 'View', 'isDay']).count()
    cnt_result.to_excel('./mySelection_count_result.xlsx')

    # 2. line별 이미지 수
    line_result = myDFs.groupby(['Line', 'View', 'isDay']).count()
    line_result.to_excel('./mySelection_line_result.xlsx')

    # 3. 낮밤으로 구분
    DN_result = myDFs.groupby(['isDay', 'View']).count()
    DN_result.to_excel('./mySelection_DN_result.xlsx')


# 엑셀 파일을 읽어와 dataframe으로 변환
myDF = pd.read_excel('/home/hyeonji/New_storage/myDF.xlsx')

# V2이미지, Position이 극단지역 제외하고 t1_pool_list에 저장
t1_pool_list = myDF.loc[(myDF['View'] != 'V1') & (myDF['Position'] != 'P01') & (myDF['Position'] != 'P02') & (myDF['Position'] != 'P03')]

# t1의 index범위 내에서 1500개 숫자 중복없이 랜덤으로 뽑기
select_list = np.random.choice(t1_pool_list.index.values, size=1500,replace=False)

#select list에 저장된 인덱스값이 될 숫자 리스트를 참고하여 t1에 있는 대상 행을 mySelection으로 옮기기
mySelection = t1_pool_list.loc[select_list]

#다만 새로운 열이 이름으로 unnamed가 추가되니 t1에서의 index라는 의미로 ori_idx로 변경
#mySelection.columns = ['ori_idx','filename', 'Date', 'Time', 'Line', 'View', 'Position', 'Rootdirs', 'isDay']

#index번호가 t1에서의 인덱스번호로 저장되어 지저분 하므로 다시 0부터 새로 부여한다 => reset
mySelection.reset_index(inplace=True)

#왜인지 새로 생긴 column들 제거
mySelection.drop([mySelection.columns[0],mySelection.columns[1]], axis=1,inplace=True)

#확인용(삭제가능)
print(mySelection.info())

#뽑기 결과로 나온 데이터프레임을 엑셀로 저장
sort_analyze_df(mySelection)
mySelection.to_excel('./myselections.xlsx')





