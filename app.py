import streamlit as st
import pandas as pd

#.\venv\Scripts\activate
# python -m streamlit run app.py 開発始めるときはこの２文 


st.title('バイト給与・年収計算ダッシュボード')

with st.sidebar:
  st.header("⚙️ 設定・入力")
  
  hourly_wage = st.number_input("時給（円）", value = 1000, step= 10)
  
  
  with st.expander("月別の勤務時間"):
      monthly_hours_list = [] #1月から12月それぞれの勤務データを格納
      for s in range(1,13):
        monthly_workhours = st.number_input(f"{s}月の労働時間" , value= 40, step = 1)
        monthly_hours_list.append(monthly_workhours)








#給料の裏側計算ロジック
annual_workhours = sum(monthly_hours_list) #年間総労働時間

monthly_salary_list = []# 1～12月　月収リスト

for m in monthly_hours_list: #1~12月それぞれの勤務時間を取り出し、時給をかけて、月収リストにぶち込む
  monthly_salary = hourly_wage * m
  monthly_salary_list.append(monthly_salary)


annual_income = hourly_wage * annual_workhours #見込み年収



#収入の画面表示
m_col1, m_col2 = st.columns(2)

with m_col1:
  st.metric(label = "月収（見込み）" , value= f"{monthly_salary:,} 円")

with m_col2:
  st.metric(label= "年収（見込み）" , value=f"{annual_income:,} 円")




#年収判定ロジック
if annual_income <= 1030000:
  remaining = 1030000 - annual_income
  st.success("103万円の壁の範囲内です!「扶養控除内」あと　" + f"{remaining:,}円稼げます。")

elif annual_income <= 1060000:
  remaining = 1060000 - annual_income
  st.info("103万の壁を越えました！106万円まであと " + f"{remaining:,} 円稼げます。 " )

elif annual_income <= 1300000:
  remaining = 1300000 - annual_income
  st.warning("106万円の壁を超えました！社会保険加入の対象になる可能性があります。130万円まであと " + f"{remaining:,} 円稼げます。")
else:
  remaining = abs(1300000 - annual_income)
  st.error("130万円の壁を越えました！親の社会保険扶養から外れます【 " + f"{remaining:,}円超過】")

ratio = min(annual_income / 1300000 , 1.0)

#年収進捗バーの設置
bar_col1, bar_col2, bar_col3 = st.columns([1,3,1])
with bar_col1:
  st.caption(f"[現在: {annual_income:,}円]")

with bar_col2:
  st.progress(ratio)

with bar_col3:
  st.caption(f"[上限: {130}万円]")

  








data = {
  "月": [f"{i}月" for i in range(1,13)],
  "月収": monthly_salary_list
}

df = pd.DataFrame(data)


#グラフの画面表示
st.subheader("月別給与推移") #中見出し
st.bar_chart(df, x="月" , y= "月収")

#Pandas データ分析　最高・最低月収・平均
max_salary = df["月収"].max()
min_salary = df["月収"].min()
avg_salary = int(df["月収"].mean())

#分析結果を表示
n_col1, n_col2, n_col3 = st.columns(3)
with n_col1:
  st.metric(label= "最高月収" , value=f"{max_salary:,}円")

with n_col2:
  st.metric(label= "最低月収", value=f"{min_salary:,}円")

with n_col3:
  st.metric(label= "平均月収", value=f"{avg_salary:,}円")




