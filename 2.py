import os
import re
import logging
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

def clean_filename(filename):
    # 替换连续的标点符号和空白字符为单个下划线，并确保不以下划线结尾
    filename = re.sub(r'[\W_]+', '_', filename)
    return filename.rstrip('_')  # 移除字符串末尾的下划线

chrome_options = Options()
chrome_options.add_argument("--headless")

driver_path = "C:\\Users\\ykla\\chromedriver.exe"
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

if os.path.exists('SEP'):
    os.rename('SEP', 'SEP_old')
if not os.path.exists("SEP"):
    os.makedirs("SEP")

with open("1.txt", "r", encoding='utf-8') as f:
    links = f.readlines()

failed_links = []
total_titles = len(links)

with tqdm(total=total_titles, desc="进度") as pbar:
    for link in links:
        link = link.strip()
        link_parts = link.split(": ")
        if len(link_parts) == 2:
            title = link_parts[0].strip().replace(" ", "")
            link = link_parts[1]

            # 提取entries/后面的内容作为文件名
            entry_content = link.split('https://plato.stanford.edu/entries/')[1]
            filename = clean_filename(entry_content)  # 清理文件名

            logging.info(f"正在抓取链接: {link}")
            try:
                driver.get(link)
                if driver.title:
                    logging.info("成功连接到网站")

                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, 'html.parser')
                    content_div = soup.find('div', {'id': 'content'})
                    if content_div:
                        content = content_div.get_text(separator='\n')
                        file_path = os.path.join("SEP", f"{filename}.txt")
                        if not os.path.exists(file_path):
                            with open(file_path, "w", encoding='utf-8') as f:
                                f.write(content)
                            logging.info(f"成功写入内容到文件: {file_path}")
                        else:
                            logging.warning(f"文件已存在: {file_path}。跳过。")
                    else:
                        logging.warning("无法在页面上找到内容。")
                else:
                    logging.warning("连接失败")
            except Exception as e:
                logging.error(f"抓取链接失败: {link}。错误: {e}")
                failed_links.append(link)
        
        pbar.update(1)

driver.quit()

if failed_links:
    logging.error("无法抓取以下链接:")
    for link in failed_links:
        logging.error(link)
