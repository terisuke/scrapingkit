# Scraping kit

## 紹介と使い方

- scraping_from_url.py は、Bing Image Search APIを使って画像をスクレイピングするスクリプトです。
- 使い方は、`python scraping_from_url.py` で実行します。
- 画像の保存先は、save_dir_path で指定します。
- 検索ワードは、search_word で指定します。
- 画像の枚数は、max_count で指定します。
- 画像のサイズは、image_size で指定します。
- scraper.pyは、ChromeDriverを使ってスクレイピングするスクリプトです。
- gspreadを使って、Googleスプレッドシートに書き込みます。
- 使い方は、`python scraper.py` で実行します。

## 工夫した点

- それぞれ別のAPIを使い、片方はフォルダに、もう片方はGoogleスプレッドシートに保存するようにしました。

## 苦戦した点

- APIごとに使うライブラリが違い、それぞれのライブラリの使い方を調べるのに時間がかかりました。

## 参考にした web サイトなど

- <https://qiita.com/bstr13/items/2856c22483d32673bca0>
  <https://qiita.com/bstr13/items/16c3761884c680f6817f>
  <https://mori-memo.hateblo.jp/entry/2023/05/06/152208#OAuth-%E5%90%8C%E6%84%8F%E7%94%BB%E9%9D%A2%E3%81%AE%E8%A8%AD%E5%AE%9A>
