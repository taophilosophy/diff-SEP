import os
import re
from datetime import datetime

# 检查有无空文件check_time，如果存在，则重命名time.log和SEP文件夹
if os.path.exists('check_time'):
    if os.path.exists('time.log'):
        os.rename('time.log', 'time_old.log')

# 定义SEP文件夹路径
SEP_folder_path = 'SEP'

# 读取SEP文件夹中的文件时间戳
new_entries = {}
for filename in os.listdir(SEP_folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(SEP_folder_path, filename)
        print("正在处理文件:", file_path)

        # 打开当前txt文件
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

            # 使用正则表达式匹配时间戳，包括只有First published的情况
            timestamps = re.findall(r'First published (.+?)(?:; substantive revision (.+?))?\n', file_content)

            # 如果没有匹配到时间戳，则跳过当前文件
            if not timestamps:
                print("未找到时间戳:", filename)
                continue

            # 转换日期格式为年-月-日
            formatted_timestamps = []
            for timestamp in timestamps:
                try:
                    published_date = datetime.strptime(timestamp[0], "%a %b %d, %Y").strftime("%Y-%m-%d")
                    revision_date = datetime.strptime(timestamp[1], "%a %b %d, %Y").strftime("%Y-%m-%d") if timestamp[1] else "N/A"
                    formatted_timestamps.append((published_date, revision_date))
                except ValueError:
                    print(f"无效的时间戳格式: {timestamp}")

            if formatted_timestamps:
                new_entries[filename] = formatted_timestamps[0]

# 将找到的时间戳写入time.log
with open('time.log', 'w', encoding='utf-8') as f:
    for filename, timestamps in new_entries.items():
        f.write(f"{filename}: First published-{timestamps[0]}")
        if timestamps[1] != "N/A":
            f.write(f", substantive revision-{timestamps[1]}")
        f.write("\n")

# 对比time.log与time_old.log，并写入diff.log
if os.path.exists('time_old.log'):
    with open('time_old.log', 'r', encoding='utf-8') as f:
        old_entries = {line.split(": ")[0].strip(): line.strip() for line in f.readlines()}
    with open('time.log', 'r', encoding='utf-8') as f:
        new_entries = {line.split(": ")[0].strip(): line.strip() for line in f.readlines()}

    added = {k: v for k, v in new_entries.items() if k not in old_entries}
    removed = {k: v for k, v in old_entries.items() if k not in new_entries}
    changed = {k: new_entries[k] for k in old_entries if k in new_entries and old_entries[k] != new_entries[k]}

    # 写入diff.log
    with open('diff.log', 'w', encoding='utf-8') as f:
        # 打印有更新的详细内容到控制台
        print("有更新的详细内容：")
        for filename, entry in added.items():
            print(f'新增-{filename}: {entry.split(": ")[1]}')
            f.write(f'新增-{filename}: {entry.split(": ")[1]}\n')
        for filename, entry in removed.items():
            print(f'减少-{filename}: {entry.split(": ")[1]}')
            f.write(f'减少-{filename}: {entry.split(": ")[1]}\n')
        for filename, entry in changed.items():
            old_entry = old_entries[filename]
            print(f'有变更-{filename}: {old_entry.split(": ")[1]} -> {entry.split(": ")[1]}')
            f.write(f'有变更-{filename}: {old_entry.split(": ")[1]} -> {entry.split(": ")[1]}\n')

# 创建空文件check_time
with open('check_time', 'w', encoding='utf-8') as f:
    pass