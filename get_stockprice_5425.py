# 操作 browser 的 驅動程式
from selenium import webdriver

# 負責開啟和關閉 Chrome 的套件
from selenium.webdriver.chrome.service import Service

# 自動下載 Chrome Driver 的套件
from webdriver_manager.chrome import ChromeDriverManager

# 例外處理的工具
from selenium.common.exceptions import TimeoutException

# 面對動態網頁，等待、了解某個元素的狀態，通常與 exptected_conditions 和 By 搭配
from selenium.webdriver.support.ui import WebDriverWait

# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC

# 期待元素出現要透過什麼方式指定，經常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By

# 強制停止/強制等待 (程式執行期間休息一下)
from time import sleep

# 隨機取得 User-Agent
from fake_useragent import UserAgent
ua = UserAgent()

# 匯入os
import os

# 啟動瀏覽器工具的選項
my_options = webdriver.ChromeOptions()
my_options.add_argument("--start-maximized")         # 最大化視窗
# my_options.add_argument("--incognito")               # 開啟無痕模式
my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
my_options.add_argument("--disable-notifications")   # 取消通知
my_options.add_argument(f'--user-agent={ua.random}') # (Optional)加入 User-Agent

# 建立下載路徑/資料夾，不存在就新增 (os.getcwd() 會取得當前的程式工作目錄)
folderPath = os.path.join(os.getcwd(), 'files')
if not os.path.exists(folderPath):
    os.makedirs(folderPath)
    
# 取得目前的路徑 aka 'pwd' in shell
# os.getcwd()

# 確認folderPath路徑有沒有正確
# folderPath

# 預設下載路徑到folderPath
my_options.add_experimental_option('prefs', {
    'download.default_directory': folderPath
})

# 造訪網站
url_history = 'https://invest.cnyes.com/twstock/TWS/5425/history#fixed'
url_institution = 'https://invest.cnyes.com/twstock/TWS/5425/holders/institution#fixed'

# 使用Chrome的WebDriver
driver = webdriver.Chrome(
    options = my_options,
    service = Service(ChromeDriverManager().install())
)

#選擇器字串
# 找到Cookie的區域
cookieBtn = "button._2nAET"
# 找到可以選擇區間的區塊
periodBtn = "div.jsx-197276814.date_picker > button.jsx-197276814.picker_btn"
#  篩選欲查詢的period
yearBtn = "div.jsx-197276814.picker_period > button" # 5yrs -> index=6
# 找到"套用"period的按鈕(但因為html格式並非form,故不能直接submit())
submitBtn = "button.jsx-197276814.action_submit"
# 選擇套用後, 即可點擊下載, 需要設定預設存取資料夾
downloadBtn = "div.jsx-2922047893.jsx-1160283235.table_action > a"

# 走訪頁面
def visit_history():
    driver.get(url_history)
    
def visit_institution():
    driver.get(url_institution)

def agree_cookie():
    try:
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, cookieBtn)
            )
        )
        sleep(2)
        
        # 同意cookie啦, 哪次不同意
        agreeBtn = driver.find_element(By.CSS_SELECTOR,cookieBtn)
        agreeBtn.click()
        sleep(2)
        
    except TimeoutException:
        print("Oops, it's a timeout exception.")

# 篩選區間並下載
def filter_n_download():
    try:
        # 等待篩選元素出現(10秒), 顯性等待
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, periodBtn)
            )
        )
        
        sleep(2)
        
        # 找到選擇區間
        trueBtn = driver.find_element(By.CSS_SELECTOR,periodBtn)
        trueBtn.click()
        sleep(2)
        # 選擇查詢區間
        five_yrBtn = driver.find_elements(By.CSS_SELECTOR,yearBtn)[6]
        five_yrBtn.click()
        sleep(2)
        # 選擇套用
        applyBtn = driver.find_element(By.CSS_SELECTOR,submitBtn)
        applyBtn.click()
        sleep(2)
        # 點擊下載
        get_csvBtn = driver.find_element(By.CSS_SELECTOR,downloadBtn)
        get_csvBtn.click()
        sleep(2)

    except TimeoutException:
        print("Oops, it's a timeout exception.")
        
# 關閉瀏覽器
def close():
    driver.quit()

if __name__=="__main__":
    visit_history()
    agree_cookie()
    filter_n_download()
    visit_institution()
    filter_n_download()
    close()