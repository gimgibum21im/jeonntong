import pandas as pd

# 데이터 준비
region_data_2019 = {
    "지역": ["경기도", "부산광역시", "서울특별시", "제주특별자치도"],
    "합계": [442393, 112504, 272907, 34908]
}

region_data_2021 = {
    "지역": ["경기도", "부산광역시", "서울특별시", "제주특별자치도"],
    "합계": [364623, 100393, 227501, 36550]
}

# 데이터프레임 생성
df_2019 = pd.DataFrame(region_data_2019)
df_2021 = pd.DataFrame(region_data_2021)


# 감소율 계산
decrease_rate = ((df_2019["합계"] - df_2021["합계"]) / df_2019["합계"] * 100).round(2)

# 데이터프레임 생성
df_analysis = pd.DataFrame({
    "지역": df_2019["지역"],
    "2019 합계": df_2019["합계"],
    "2021 합계": df_2021["합계"],
    "감소율 (%)": decrease_rate,
})