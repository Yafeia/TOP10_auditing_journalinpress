import pandas as pd
from datetime import datetime

# 读取表格A
df_a = pd.read_csv("TOP10_2024-03-17.csv")

# 获取当前日期并格式化为字符串
current_date = datetime.now().strftime("%Y-%m-%d")

# 读取表格B，并将当前日期插入文件名中
df_b = pd.read_csv(f"TOP10_{current_date}.csv")

# 1. 表格A和B的合并结果，并将当前日期插入文件名中
merged_df = pd.merge(df_a, df_b, on="Title", how="outer")
merged_df.to_csv(f"merged_TOP10_{current_date}.csv", index=False)

# 2. 删除B中在A中已经存在的结果并保存在表格C
existing_titles = df_a["Title"].unique()
filtered_df_b = df_b[~df_b["Title"].isin(existing_titles)]
filtered_df_b.to_csv(f"TOP10新增_{current_date}.csv", index=False)
