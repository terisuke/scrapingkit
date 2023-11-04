from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import gspread
import os

# WebDriverを初期化
driver = webdriver.Chrome(ChromeDriverManager().install())

# トップページにアクセス
driver.get('https://works.litalico.jp/center/')

# 各地域のページへのリンクを取得
region_links = [a.get_attribute('href') for a in driver.find_elements_by_css_selector('.areaList a')]

# gspreadで認証とスプレッドシートの初期化
dir_path = os.path.dirname(__file__)
gc = gspread.oauth(
    credentials_filename=os.path.join(dir_path, "client_secret.json"),
    authorized_user_filename=os.path.join(dir_path, "authorized_user.json"),
)
wb = gc.create("AllCentersData")
worksheet = wb.get_worksheet(0)

# ヘッダー行を追加
worksheet.append_row(['事業所名', '住所', 'アクセス', '電話番号'])

# 各地域のページに移動し、データを抽出
for region_link in region_links:
    driver.get(region_link)
    center_ids = [element.get_attribute('id') for element in driver.find_elements_by_css_selector('.centerList .centerElement')]
    for center_id in center_ids:
        element1_link = driver.find_element_by_xpath(f'//*[@id="{center_id}"]/div[1]/a').get_attribute('href')
        element2 = driver.find_element_by_xpath(f'//*[@id="{center_id}"]/div[2]/div[2]/div[1]/div[1]/div').text
        element3 = driver.find_element_by_xpath(f'//*[@id="{center_id}"]/div[2]/div[2]/div[1]/div[2]/div').text
        element4_tel = driver.find_element_by_xpath(f'//*[@id="{center_id}"]/div[2]/div[2]/div[1]/div[3]/div/a').get_attribute('href').replace('tel:', '')
        # データをスプレッドシートに保存
        worksheet.append_row([element1_link, element2, element3, element4_tel])

# WebDriverを閉じる
driver.quit()