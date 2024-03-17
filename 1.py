import os
import requests
from bs4 import BeautifulSoup

def fetch_and_write_links(url, filename):
    try:
        print("正在连接到目录地址...")
        response = requests.get(url)
        print("连接成功！")

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        entries_count = 0
        unique_entries = set()  # 用于存储唯一的entries/后面的内容

        with open(filename, 'w', encoding='utf-8') as f:
            for link in links:
                text = link.text.strip()
                href = link.get('href')

                if href and href.startswith('entries/'):
                    entry_id = href.split('entries/')[1]  # 获取entries/后面的内容
                    if entry_id not in unique_entries:
                        unique_entries.add(entry_id)
                        entries_count += 1
                        full_url = 'https://plato.stanford.edu/' + href
                        line = f"{text}: {full_url}\n"
                        f.write(line)
                        print(f"写入链接：{line.strip()}")
                    else:
                        print(f"重复的entries/内容已排除：{entry_id}")

        print("爬取完成！包含'entries'的链接数量为：", entries_count)
        print("结果已保存到", filename)
    
    except requests.RequestException as e:
        print("请求页面内容时发生错误：", e)

def compare_and_output_diff():
    if os.path.exists("1_old.txt"):
        with open('1.txt', 'r', encoding='utf-8') as f1, open('1_old.txt', 'r', encoding='utf-8') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()

        new_entries = [line for line in lines1 if line not in lines2]
        missing_entries = [line for line in lines2 if line not in lines1]

        with open('diff_txt.txt', 'w', encoding='utf-8') as f_diff:
            if new_entries:
                f_diff.write("新增的条目：\n")
                f_diff.writelines(new_entries)
            if missing_entries:
                f_diff.write("缺少的条目：\n")
                f_diff.writelines(missing_entries)

        if new_entries:
            print("新增的条目：")
            for entry in new_entries:
                print(entry.strip())
        if missing_entries:
            print("缺少的条目：")
            for entry in missing_entries:
                print(entry.strip())
    else:
        print("不存在 1_old.txt 文件，无法进行比较。")

def main():
    if os.path.exists("check_time"):
        if os.path.exists("1.txt"):
            os.rename("1.txt", "1_old.txt")
    else:
        if os.path.exists("1.txt"):
            os.remove("1.txt")

    url = "https://plato.stanford.edu/contents.html"
    fetch_and_write_links(url, '1.txt')
    compare_and_output_diff()

    with open("check_time", "w") as check_file:
        pass

if __name__ == "__main__":
    main()