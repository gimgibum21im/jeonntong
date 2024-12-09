import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)

# 파일 경로 설정
file_paths_2019 = {
    "01": "src/상가업소_201906/소상공인시장진흥공단_상가업소정보_201906_01.csv",
    "03": "src/상가업소_201906/소상공인시장진흥공단_상가업소정보_201906_03.csv",
    "04": "src/상가업소_201906/소상공인시장진흥공단_상가업소정보_201906_04.csv"
}

# 업종별 대분류 및 중분류 매핑 (2019년 기준)
category_mapping_2019 = {
    "음식": ["음식"],
    "소매": ["소매"],
    "스포츠": ["스포츠", "스포츠/운동"],  # 스포츠와 스포츠/운동 통합
    "오락": ["관광/여가/오락"],  # 관광/여가/오락에서 스포츠/운동 제외
    "숙박": ["숙박"]
}

# 필요한 지역 설정
regions_01 = ['서울특별시', '부산광역시']
regions_03 = ['경기도']
regions_04 = ['제주특별자치도']

# 데이터 병합용 리스트
filtered_data_list_2019 = []

# 01 데이터 처리
data_01 = pd.read_csv(file_paths_2019["01"], encoding="utf-8")
filtered_01 = data_01[data_01["시도명"].isin(regions_01)]
filtered_data_list_2019.append(filtered_01)

# 03 데이터 처리
data_03 = pd.read_csv(file_paths_2019["03"], encoding="utf-8")
filtered_03 = data_03[data_03["시도명"].isin(regions_03)]
filtered_data_list_2019.append(filtered_03)

# 04 데이터 처리
data_04 = pd.read_csv(file_paths_2019["04"], encoding="utf-8")
filtered_04 = data_04[data_04["시도명"].isin(regions_04)]
filtered_data_list_2019.append(filtered_04)

# 모든 데이터를 병합
merged_data_2019 = pd.concat(filtered_data_list_2019, ignore_index=True)

# 대분류와 중분류를 기준으로 분류 추가
def categorize(row):
    # 스포츠 분류: 대분류가 스포츠이거나 중분류가 스포츠/운동 또는 학문/교육 내 학원-예능취미체육인 경우
    if (row["상권업종대분류명"] == "스포츠" or 
        row["상권업종중분류명"] == "스포츠/운동" or 
        (row["상권업종대분류명"] == "학문/교육" and row["상권업종중분류명"] == "학원-예능취미체육")):
        return "스포츠"
    # 오락에서 스포츠/운동 제외한 관광/여가/오락
    elif row["상권업종대분류명"] == "관광/여가/오락" and row["상권업종중분류명"] != "스포츠/운동":
        return "오락"
    # 기타 분류
    for key, values in category_mapping_2019.items():
        if row["상권업종대분류명"] in values:
            return key
    return None

# 분류 추가
merged_data_2019["분류"] = merged_data_2019.apply(categorize, axis=1)

# 유효한 업종만 필터링
merged_data_2019 = merged_data_2019.dropna(subset=["분류"])

# 지역 및 업종별 데이터 집계
region_category_totals_2019 = merged_data_2019.pivot_table(
    index="분류",
    columns="시도명",
    aggfunc="size",
    fill_value=0
)

# 총계 계산
region_category_totals_2019["합계"] = region_category_totals_2019.sum(axis=1)
total_row_2019 = pd.DataFrame(region_category_totals_2019.sum(axis=0)).T
total_row_2019.index = ["합계"]

# 총계 행 추가
region_category_totals_2019 = pd.concat([region_category_totals_2019, total_row_2019])

# 전체 데이터 개수 분의 업종 합계를 계산한 열 추가
total_data_count_2019 = region_category_totals_2019.loc["합계", "합계"]
region_category_totals_2019["비율"] = (region_category_totals_2019["합계"] / total_data_count_2019).round(6)

# 결과 출력

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows: 맑은 고딕
plt.rcParams["axes.unicode_minus"] = False    # 마이너스 기호 깨짐 방지

# 데이터 준비
columns = region_category_totals_2019.columns
data = region_category_totals_2019.reset_index().values

# 그래프 크기 설정
fig, ax = plt.subplots(figsize=(10, 5))
ax.axis("tight")  # 축 제거
ax.axis("off")    # 축 제거

# 표 생성
table = ax.table(
    cellText=data,
    colLabels=["2019"] + list(columns),
    cellLoc="center",
    loc="center",
    colColours=["#404040"] * (len(columns) + 1)  # 헤더 색상 + ["#f0f0f0"]
)

# 스타일 설정
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(columns) + 1)))  # 컬럼 폭 자동 조정

# 각 행 높이 설정
for (row, col), cell in table.get_celld().items():
    if row == 0:  # 헤더 행
        cell.set_fontsize(12)
        cell.set_height(0.15)  # 헤더 높이
        cell.set_text_props(weight="bold", color="white")  # 헤더 텍스트 스타일
    else:
        cell.set_height(0.1)  # 데이터 행 높이

# 출력
plt.show()
