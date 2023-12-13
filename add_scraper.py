from selenium import webdriver  # Seleniumのwebdriverモジュールをインポート
from selenium.webdriver.common.by import By  # SeleniumのByモジュールをインポート
from selenium.webdriver.support.ui import WebDriverWait  # SeleniumのWebDriverWaitモジュールをインポート
from selenium.webdriver.support import expected_conditions as EC  # Seleniumのexpected_conditionsモジュールをインポート
from bs4 import BeautifulSoup  # BeautifulSoupをインポート
import pandas as pd  # pandasをインポート
browser = webdriver.Chrome()  # ChromeのWebDriverをインスタンス化
browser.get('https://jinzai.hellowork.mhlw.go.jp/JinzaiWeb/GICB101010.do?action=initDisp&screenId=GICB101010')  # 求人情報のページにアクセス
browser.execute_script("doPostAction('transition', '1')")  # JavaScriptを実行してページを遷移
WebDriverWait(browser, 10).until(  # 10秒以内に要素がクリッカブルになるまで待機
    EC.element_to_be_clickable((By.ID, 'ID_cbZenkoku1'))
)
elem_click_btn = browser.find_element(By.ID,'ID_cbZenkoku1')  # 要素を取得
elem_click_btn.click()  # 要素をクリック
WebDriverWait(browser, 10).until(  # 10秒以内に要素がクリッカブルになるまで待機
    EC.element_to_be_clickable((By.XPATH, "//input[@id='id_btnSearch' and @src='jsp/img/button/search_button.gif']"))
)
elem_start_btn = browser.find_element(By.XPATH,"//input[@id='id_btnSearch' and @src='jsp/img/button/search_button.gif']")  # 要素を取得
elem_start_btn.click()  # 要素をクリック
target_page = 1739  # 目標ページ数を設定
current_page = 1  # 現在のページを初期化
output_path = '/Users/teradakousuke/Library/Mobile Documents/com~apple~CloudDocs/Scriping tool/hellowork.csv'  # 出力先のパスを指定
data = []  # データを格納するリストを初期化
try:  # 例外処理
    existing_data = pd.read_csv(output_path)  # 既存のデータを読み込む
except FileNotFoundError:  # ファイルが見つからない場合の例外処理
    existing_data = pd.DataFrame(columns=['事業主名', '事業所名', '事業所住所', '電話番号', '就職者数（有期）', '就職者数（無期）', '就職者数（2年有期）', '詳細情報'])  # 列名を指定して空のDataFrameを作成

while current_page <= target_page:  # 現在のページが目標ページ以下の間ループ
    try:  # 例外処理
        page_source = browser.page_source  # ページのソースを取得
        soup = BeautifulSoup(page_source, 'html.parser')  # BeautifulSoupを使用してページのソースを解析
        elements_jigyonushi_name = soup.find_all('span', id='ID_lbJigyonushiName')  # 全ての事業主名の要素を取得
        num_items = len(elements_jigyonushi_name)  # 要素の数を取得
        
        for i in range(num_items):  # 要素の数だけループ
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
            next_page_button = browser.find_elements(By.ID, 'ID_pager02')  # 次のページボタンを取得
            if not next_page_button:  # 次のページボタンがない場合
                print("最終ページに到達しました。")  # メッセージを出力
                break  # ループを抜ける
            browser.execute_script(f"doPostAction('page', '{current_page + 1}')")  # JavaScriptを実行して次のページに遷移
            WebDriverWait(browser, 10).until(  # 10秒以内に要素が存在するまで待機
                EC.presence_of_element_located((By.ID, "ID_linkKyokatodokedeNo"))
            )
        current_page += 1  # 現在のページを更新
    except Exception as e:  # 例外処理
        print(f"ページ遷移中にエラーが発生しました: {e}")  # エラーメッセージを出力
        break  # ループを抜ける
new_data = pd.DataFrame(data, columns=['事業主名', '事業所名', '事業所住所', '電話番号', '就職者数（有期）', '就職者数（無期）', '就職者数（2年有期）', '詳細情報'])  # データをDataFrameに変換
final_data = pd.concat([existing_data, new_data]).drop_duplicates()  # 既存のデータと新しいデータを結合して重複を削除

final_data.to_csv(output_path, index=False, encoding='utf-8')  # DataFrameをCSVファイルとして出力
browser.quit()  # ブラウザを終了
