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
my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
my_options.add_argument("--disable-notifications")   # 取消通知
my_options.add_argument(f'--user-agent={ua.random}') # (Optional)加入 User-Agent

# 建立下載路徑/資料夾，不存在就新增 (os.getcwd() 會取得當前的程式工作目錄)
folderPath = os.path.join(os.getcwd(), 'files')
if not os.path.exists(folderPath):
    os.makedirs(folderPath)
    
# 預設下載路徑到folderPath
my_options.add_experimental_option('prefs', {
    'download.default_directory': folderPath
})

# 自行填入參數
# 目標網站 - 可提供股市與各分點的資料
url = 'https://histock.tw/stock/branch.aspx?no=5425&from=20230210&to=20230210'
email = "abcdefg@gmail.com"
password = "abcdefg"

# 使用Chrome的WebDriver
driver = webdriver.Chrome(
    options=my_options,
    service=Service(ChromeDriverManager().install())
)

# 用來存放分點的list
institution_lists = []

def visit_website(url, email, password):

    driver.get(url)

    # 點選彈出裡面的確定按鈕
    # driver.switch_to.alert.accept()

    login = driver.find_element(By.CSS_SELECTOR, "#login")
    login.click()
    email_field = driver.find_element(By.CSS_SELECTOR, "input#email")
    email_field.send_keys(email)
    pwd = driver.find_element(By.CSS_SELECTOR, "input#password")
    pwd.send_keys(password)
    login_2 = driver.find_element(By.CSS_SELECTOR, "input#bLogin")
    login_2.click()



def get_institution_lists(driver):
    global institution_lists
    count = 0

    while count < 10:  # 選10個交易日的資料
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a#CPHB1_Branch1_hlDayPre")
                )
            )
            print(count)
            sleep(2)
            # 先清空institutions
            institutions = []
            # 找到分點名稱
            institutions = [i.text for i in driver.find_elements(By.CSS_SELECTOR, "td > a")]
            # 如果分點長度=0, 代表當天沒開盤, 繼續往前一天, count不計
            if len(institutions) == 0:
                oneday_before = driver.find_element(By.CSS_SELECTOR, '#CPHB1_Branch1_hlDayPre')
                oneday_before.click()
                sleep(2)
                # 檢查點
                print('skip')
            else:
                for i in institutions:
                    # 如果分點名稱不在list裡面才加進institution_lists,避免重複
                    if i not in institution_lists:
                        institution_lists.append(i)
                # 檢查點
                print(institutions)
                print('done')
                count += 1
                oneday_before = driver.find_element(By.CSS_SELECTOR, '#CPHB1_Branch1_hlDayPre')
                oneday_before.click()

        except TimeoutException:
            print("oops")
        except UnexpectedAlertPresentException:
            print("I'm afraid I need to login.")

    return institution_lists

def write_to_csv(folder_path, institution_lists):
    with open(folder_path, 'w') as file:
        for i in institution_lists:
            file.write(i)
            file.write(',')


if __name__ == '__main__':
    visit_website(url, email, password)
    get_institution_lists(driver)
    driver.quit()
    write_to_csv(folder_path=folderPath, institution_lists=institution_lists)

