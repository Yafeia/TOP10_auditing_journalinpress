import subprocess

# 定义要执行的 py 文件列表
python_files = ['AOS-JAE.py',
                 'JAR.py',
                 'JFE.py',
                 'MS.py',
                 'RAS.py',
                 'RFS.py',
                 'TAR.py',
                 'wiley-JAR-CAR-TJF.py',
                ]

# 依次执行每个 py 文件
for file in python_files:
    subprocess.run(['python', file])

print("所有文件执行完毕")
