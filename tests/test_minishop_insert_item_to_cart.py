#!/usr/bin/env python

# selenium使います
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging

# テスト用のライブラリ
import unittest

# ロガーを作成、出力先はstdout, ログレベルはINFO
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# テスト用のサーバー(Selenium grid)
REMOTE_URL = "http://selenium:4444/wd/hub"

class TestCase(unittest.TestCase):

    # 今の時間のタイムスタンプを生成しておく(テスト時に結果ファイルに付けるため)
    timestamp = None

    def setUp(self):
        # timestampがNoneの場合、現在時刻を取得
        if self.timestamp is None:
            from datetime import datetime
            self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # selenium gridのサーバーに接続
        self.driver = webdriver.Remote(REMOTE_URL, options=webdriver.ChromeOptions())

    def tearDown(self):
        # テストサーバー切断
        self.driver.quit()
        # public/testcase.htmlおよびpublic/testcase.phpを削除
        import os

    # 接続して、ジャンルを選択して商品一覧を取得するテスト
    def test_access(self):
        self.driver.get("http://web/")
        # ラジオボタン、name=genreの要素から、value=pcを選択
        genre = self.driver.find_elements(By.NAME, "genre")
        genre[0].click()
        self.driver.get_screenshot_as_file(f"results/{self.timestamp}-01-select-pc.png")

        # 送信ボタンをクリック
        self.driver.find_element(By.XPATH, "/html/body/form/input[2]").click()

        # 5番目の項目の「詳細」リンクをクリックする
        logger.info(self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr[6]/td[2]").text) # macBook Pro
        self.assertIn("MacBook Pro", self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr[6]/td[2]").text)
        # テキスト部分をマウスでなぞった感じでテキストの色反転をさせる
        self.driver.execute_script("arguments[0].style.color='red';", self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr[6]/td[5]"))
        self.driver.get_screenshot_as_file(f"results/{self.timestamp}-02-list-pc.png")

        link = self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr[6]/td[5]/a")
        link.click()
        self.driver.get_screenshot_as_file(f"results/{self.timestamp}-03-detail-macbook.png")

        # カートに入れるためsubmitのボタンをクリックする
        self.driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[6]/th/input").click()
        self.driver.execute_script("arguments[0].style.color='red';", self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[2]"))
        self.driver.get_screenshot_as_file(f"results/{self.timestamp}-04-insert-to-cart.png")
        self.assertEqual("MacBook Pro", self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[2]").text)




if __name__ == "__main__":
    unittest.main()
