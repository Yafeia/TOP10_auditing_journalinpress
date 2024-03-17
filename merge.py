import csv
from datetime import datetime

current_date = datetime.now().strftime('%Y-%m-%d')
source_csv_files = [
    f'文献_{current_date}.csv',
    f'文献_AOS_JAE_{current_date}.csv',
    f'文献_JAR_{current_date}.csv',
    f'文献_JFE_{current_date}.csv',
    f'文献_MS_{current_date}.csv',
    f'文献_RAS_{current_date}.csv',
    f'文献_TAR_{current_date}.csv',
]

merged_csv_file = 'TOP10_{current_date}.csv'

# 创建目标 CSV 文件
with open(merged_csv_file, mode='w', newline='', encoding='utf-8') as merged_file:
    writer = csv.writer(merged_file)
    
    # 写入 CSV 文件的表头
    header_written = False

    # 逐个读取每个源 CSV 文件，并将其内容写入目标 CSV 文件
    for source_csv_file in source_csv_files:
        with open(source_csv_file, mode='r', newline='', encoding='utf-8') as source_file:
            reader = csv.reader(source_file)
            
            # 逐行写入源 CSV 文件的内容（不包括表头）
            for row in reader:
                if not header_written:  # 写入目标 CSV 文件的表头
                    writer.writerow(row)
                    header_written = True
                else:
                    writer.writerow(row)

print(f'Merged data has been successfully written to {merged_csv_file}')
