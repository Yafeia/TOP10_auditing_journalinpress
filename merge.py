import csv
from datetime import datetime

current_date = datetime.now().strftime('%Y-%m-%d')
source_csv_files = [
    f'文献_JAR_CAR_TJF{current_date}.csv',
    f'文献_AOS_JAE_{current_date}.csv',
    f'文献_JAR_{current_date}.csv',
    f'文献_JFE_{current_date}.csv',
    f'文献_MS_{current_date}.csv',
    f'文献_RAS_{current_date}.csv',
    f'文献_TAR_{current_date}.csv',
]


# 重新定义目标 CSV 文件名
merged_csv_file = f'TOP10_{current_date}.csv'

# 定义输出日期格式
output_date_format = '%Y-%m-%d'  # 输出日期格式为 YYYY-MM-DD

# 创建目标 CSV 文件
with open(merged_csv_file, mode='w', newline='', encoding='utf-8-sig') as merged_file:
    writer = csv.writer(merged_file)
    
    # 写入 CSV 文件的表头
    header_written = False

    # 逐个读取每个源 CSV 文件，并将其内容写入目标 CSV 文件
    for source_csv_file in source_csv_files:
        with open(source_csv_file, mode='r', newline='', encoding='utf-8-sig') as source_file:
            reader = csv.reader(source_file)
            
            # 逐行写入源 CSV 文件的内容（不包括表头）
            for row in reader:
                if not header_written:  # 写入目标 CSV 文件的表头
                    writer.writerow(row)
                    header_written = True
                else:
                    # 对 Publication Date 字段进行格式转换
                    publication_date_index = 2  # 假设 Publication Date 字段在 CSV 中的索引为 2
                    try:
                        original_value = row[publication_date_index]
                        if original_value.strip():  # 检查字段值是否非空
                            try:
                                # 尝试多种日期格式
                                date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y', '%Y/%m/%d', '%Y%m%d']
                                parsed_date = None
                                for date_format in date_formats:
                                    try:
                                        parsed_date = datetime.strptime(original_value, date_format)
                                        break
                                    except ValueError:
                                        continue
                                
                                if parsed_date:
                                    formatted_date = parsed_date.strftime(output_date_format)
                                    row[publication_date_index] = formatted_date
                                else:
                                    row[publication_date_index] = f'{original_value}'
                            except ValueError:
                                row[publication_date_index] = f'{original_value}'
                        else:
                            row[publication_date_index] = 'N/A'  # 如果字段值为空，则设置为默认值
                    except IndexError:
                        pass  # 处理索引超出范围的情况
                    
                    writer.writerow(row)

print(f'Merged data with standardized Publication Date has been successfully written to {merged_csv_file}')
