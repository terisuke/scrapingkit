from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
browser = webdriver.Chrome()
browser.get('https://jinzai.hellowork.mhlw.go.jp/JinzaiWeb/GICB101010.do?action=initDisp&screenId=GICB101010')
browser.execute_script("doPostAction('transition', '1')")
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, 'ID_cbZenkoku1'))
)
elem_click_btn = browser.find_element(By.ID,'ID_cbZenkoku1')
elem_click_btn.click()
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@id='id_btnSearch' and @src='jsp/img/button/search_button.gif']"))
)
elem_start_btn = browser.find_element(By.XPATH,"//input[@id='id_btnSearch' and @src='jsp/img/button/search_button.gif']")
elem_start_btn.click()
target_page = 1739
current_page = 1727
output_path = '/Users/teradakousuke/Library/Mobile Documents/com~apple~CloudDocs/Scriping tool/hellowork.csv'
data = []
try:
    existing_data = pd.read_csv(output_path)
except FileNotFoundError:
    existing_data = pd.DataFrame(columns=['事業主名', '事業所名', '事業所住所', '電話番号', '就職者数（有期）', '就職者数（無期）', '就職者数（2年有期）', '詳細情報'])

while current_page <= target_page:
    try:
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        elements_jigyonushi_name = soup.find_all('span', id='ID_lbJigyonushiName')
        num_items = len(elements_jigyonushi_name)
        
        for i in range(num_items):
            jigyonushi_name = soup.find_all('span', id='ID_lbJigyonushiName')[i].get_text(strip=True)
            jigyosho_name = soup.find_all('span', id='ID_lbJigyoshoName')[i].get_text(strip=True)
            jigyosho_address = soup.find_all('span', id='ID_lbJigyoshoAddress')[i].get_text(strip=True)
            tel = soup.find_all('span', id='ID_lbTel')[i].get_text(strip=True)
            shushokusha1yuki3 = soup.find_all('span', id='ID_lbShushokusha1yuki3')[i].get_text(strip=True)
            shushokusha1muki3 = soup.find_all('span', id='ID_lbShushokusha1muki3')[i].get_text(strip=True)
            shushokusha2yuki3 = soup.find_all('span', id='ID_lbShushokusha2yuki3')[i].get_text(strip=True)
            detail_link = browser.find_elements(By.ID, 'ID_linkKyokatodokedeNo')[i].get_attribute('href')
        
            data.append([jigyonushi_name, jigyosho_name, jigyosho_address, tel, shushokusha1yuki3, shushokusha1muki3, shushokusha2yuki3, detail_link])
        if current_page < target_page:
            next_page_button = browser.find_elements(By.ID, 'ID_pager02')
            if not next_page_button:
                print("最終ページに到達しました。")
                break
            browser.execute_script(f"doPostAction('page', '{current_page + 1}')")
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "ID_linkKyokatodokedeNo"))
            )
        current_page += 1
    except Exception as e:
        print(f"ページ遷移中にエラーが発生しました: {e}")
        break
new_data = pd.DataFrame(data, columns=['事業主名', '事業所名', '事業所住所', '電話番号', '就職者数（有期）', '就職者数（無期）', '就職者数（2年有期）', '詳細情報'])
final_data = pd.concat([existing_data, new_data]).drop_duplicates()

final_data.to_csv(output_path, index=False, encoding='utf-8')
browser.quit()