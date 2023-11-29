import pandas as pd

# CSVファイルのパス
file_path = '/Users/teradakousuke/Library/Mobile Documents/com~apple~CloudDocs/Scriping tool/hellowork.csv'

# CSVファイルを読み込む
df = pd.read_csv(file_path)

# 事業主名、事業所名、事業所住所が同一の行を重複とみなして除去
df.drop_duplicates(subset=['事業主名', '事業所名', '事業所住所'], inplace=True)

# 変更を保存
df.to_csv(file_path, index=False, encoding='utf-8')
