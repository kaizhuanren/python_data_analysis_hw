from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式（不打开浏览器窗口）
driver = webdriver.Chrome(options=chrome_options)

ids = ['1958734', '2379124', '2930378', '3098515', '2886139', '3122717', '2901280', '2037784', '3103268', '2437623', '2835466', '2232902', '1797236', '2998706', '758781', '2940702', '3055732', '2043028', '2336694', '2368156', '1919444']
all_data = []

for user_id in ids:
    url = f'https://www.cmzj.net/expertItem?id={user_id}'
    driver.get(url)
    time.sleep(5)  # 等待 JS 加载完成
    print('正在爬取用户id{}'.format(user_id))

    # 提取姓名
    try:
        name = driver.find_element(By.CLASS_NAME, 'okami-name').text
    except:
        name = "N/A"

    # 提取彩龄
    try:
        cailing = driver.find_element(By.CSS_SELECTOR, '.okami-text > p:nth-of-type(1) > span').text
    except:
        cailing = "N/A"

    # 提取文章数量
    try:
        article_count = driver.find_element(By.CSS_SELECTOR, '.okami-text > p:nth-of-type(2) > span').text
    except:
        article_count = "N/A"

    # 提取专家简介
    try:
        intro = driver.find_element(By.CLASS_NAME, 'titleText').text
    except:
        intro = "N/A"

    # 提取彩种等级
    try:
        levels = [span.text for span in driver.find_elements(By.CSS_SELECTOR, '.czdj span')]
    except:
        levels = []

    # 提取大奖战绩

    try:
        dajiang_zhanji_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'djzjP'))
        )
        dajiang_zhanji = dajiang_zhanji_element.text.replace("大奖战绩：", "").strip()
        dajiang_zhanji = dajiang_zhanji.replace("\n", "") 
        dajiang_zhanji = dajiang_zhanji.replace("\t", "")  
        dajiang_zhanji = " ".join(dajiang_zhanji.split()) 
    except:
        dajiang_zhanji = "N/A"


    all_data.append({
        '用户ID': user_id,
        '姓名': name,
        '彩龄': cailing,
        '文章数量': article_count,
        '专家简介': intro,
        '彩种等级': levels,
        '大奖战绩': dajiang_zhanji,
    })

driver.quit()

df = pd.DataFrame(all_data)
df.to_csv("expert_data.csv", index=False, encoding='utf_8_sig')