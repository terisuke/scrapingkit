from selenium import webdriver  # seleniumライブラリからwebdriverをインポート
from selenium.webdriver.common.by import By  # seleniumのByクラスからインポート
from selenium.webdriver.support.ui import WebDriverWait  # seleniumのWebDriverWaitをインポート
from selenium.webdriver.support import expected_conditions as EC  # seleniumのexpected_conditionsをECとしてインポート
from bs4 import BeautifulSoup  # BeautifulSoupをインポート
import pandas as pd  # pandasをpdとしてインポート

browser = webdriver.Chrome()  # Chromeのwebdriverをインスタンス化
browser.get('https://jinzai.hellowork.mhlw.go.jp/JinzaiWeb/GICB101010.do?action=initDisp&screenId=GICB101010')  # 指定したURLにアクセス
browser.execute_script("doPostAction('transition', '1')")  # JavaScriptを実行してページ遷移
WebDriverWait(browser, 10).until(  # 10秒以内に待機
    EC.element_to_be_clickable((By.ID, 'ID_cbZenkoku1'))  # IDが'ID_cbZenkoku1'の要素がクリック可能になるまで待機
)
elem_click_btn = browser.find_element(By.ID,'ID_cbZenkoku1')  # IDが'ID_cbZenkoku1'の要素を取得
elem_click_btn.click()  # 要素をクリック
WebDriverWait(browser, 10).until(  # 10秒以内に待機
    EC.element_to_be_clickable((By.XPATH, "//input[@id='id_btnSearch' and @src='jsp/img/button/search_button.gif']"))  # XPathが指定条件を満たす要素がクリック可能になるまで待機
)
elem_start_btn = browser.find_element(By.XPATH,"//input[@id='id_btnSearch' and @src='jsp/img/button/search_button.gif']")  # 検索ボタンの要素を取得
elem_start_btn.click()  # 検索ボタンをクリック
target_page = 1739  # 目標ページ数を設定
current_page = 1  # 現在のページを設定
data = []  # データを格納するリストを初期化
while current_page < target_page:  # 現在のページが目標ページ未満の間繰り返す
    try:  # 例外処理を開始
        page_source = browser.page_source  # ページのソースを取得
        soup = BeautifulSoup(page_source, 'html.parser')  # BeautifulSoupでページのソースを解析
        
        for i in range(20):  # 20回繰り返す
            jigyonushi_name = soup.find_all('span', id='ID_lbJigyonushiName')[i].get_text(strip=True)  # 事業主名を取得
            jigyosho_name = soup.find_all('span', id='ID_lbJigyoshoName')[i].get_text(strip=True)  # 事業所名を取得
            jigyosho_address = soup.find_all('span', id='ID_lbJigyoshoAddress')[i].get_text(strip=True)  # 事業所住所を取得
            tel = soup.find_all('span', id='ID_lbTel')[i].get_text(strip=True)  # 電話番号を取得
            shushokusha1yuki3 = soup.find_all('span', id='ID_lbShushokusha1yuki3')[i].get_text(strip=True)  # 就職者数（有期）を取得
            shushokusha1muki3 = soup.find_all('span', id='ID_lbShushokusha1muki3')[i].get_text(strip=True)  # 就職者数（無期）を取得
            shushokusha2yuki3 = soup.find_all('span', id='ID_lbShushokusha2yuki3')[i].get_text(strip=True)  # 就職者数（2年有期）を取得
            detail_link = browser.find_elements(By.ID, 'ID_linkKyokatodokedeNo')[i].get_attribute('href')  # 詳細リンクを取得
        
            data.append([jigyonushi_name, jigyosho_name, jigyosho_address, tel, shushokusha1yuki3, shushokusha1muki3, shushokusha2yuki3, detail_link])  # データをリストに追加
        if current_page < target_page:  # 現在のページが目標ページ未満の場合
            browser.execute_script(f"doPostAction('page', '{current_page + 1}')")  # JavaScriptを実行して次のページに遷移
            WebDriverWait(browser, 10).until(  # 10秒以内に待機
                EC.presence_of_element_located((By.ID, "ID_pager11"))  # IDが'ID_pager11'の要素が存在するまで待機
            )
        current_page += 1  # 現在のページを更新
    except Exception as e:  # 例外処理
        print(f"ページ遷移中にエラーが発生しました: {e}")  # エラーメッセージを出力
        break  # ループを抜ける
df = pd.DataFrame(data, columns=['事業主名', '事業所名', '事業所住所', '電話番号', '就職者数（有期）', '就職者数（無期）', '就職者数（2年有期）', '詳細情報'])  # データをDataFrameに変換
output_path = '/Users/teradakousuke/Library/Mobile Documents/com~apple~CloudDocs/Scriping tool/hellowork.csv'  # 出力先のパスを指定
df.to_csv(output_path, index=False, encoding='utf-8')  # DataFrameをCSVファイルとして出力
browser.quit()  # ブラウザを終了
