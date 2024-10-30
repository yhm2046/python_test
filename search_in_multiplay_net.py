from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import quote

# 设置Chrome选项
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 注释掉这行以显示浏览器窗口

# 要搜索的网站
websites = [
    "https://www.minnano-av.com/",
    "https://maipenrai03.blog.2nt.com/",
    "http://sougouwiki.com/"
]

# 搜索关键词
search_query = "木下凛々子"  # 使用日语原文可能获得更好的结果

# 创建Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 打开第一个搜索结果
search_url = f"https://www.google.com/search?q={quote(search_query)}+site:{websites[0]}"
driver.get(search_url)

# 等待并点击第一个搜索结果
try:
    first_result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.g a"))
    )
    first_result.click()
except Exception as e:
    print(f"无法点击第一个网站的搜索结果: {e}")

# 打开其他搜索结果在新标签页并点击第一个结果
for website in websites[1:]:
    search_url = f"https://www.google.com/search?q={quote(search_query)}+site:{website}"
    # 打开新标签页
    driver.execute_script(f"window.open('{search_url}', '_blank');")
    time.sleep(1)  # 等待新标签页打开
    
    # 切换到新标签页
    driver.switch_to.window(driver.window_handles[-1])
    
    # 等待并点击第一个搜索结果
    try:
        first_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.g a"))
        )
        first_result.click()
    except Exception as e:
        print(f"无法点击搜索结果: {e}")

# 添加等待机制，防止浏览器自动关闭
input("按Enter键关闭浏览器...")

# 关闭浏览器
driver.quit()