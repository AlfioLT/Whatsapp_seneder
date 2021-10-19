import pyodbc

import configparser
import  webbrowser as wb
import time

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

""""Config configparser"""
config = configparser.RawConfigParser()
config.read('config.properties')

"""TimeInterval params"""
start_time_hour = config.get('TimeInterval', 'start_time_HOUR')
start_time_minute = config.get('TimeInterval', 'start_time_MINUTE')
end_time_hour = config.get('TimeInterval', 'end_time_HOUR')
end_time_minute = config.get('TimeInterval', 'end_time_MINUTE')

"""Credentials"""
selenium_path = config.get('Selenium', 'path')

"""CODBOT Config"""
codbot = config.get('CODBOT','cod')


dbc = ('Driver={SQL Server};'
        'Server=192.168.0.190;'
        'Database=FASTBOT;'
        'Uid=icox;'
        'Pwd=iAmByou#2014')

conn = pyodbc.connect(dbc)
cursor = conn.cursor()

cursor.execute("SELECT c.Cell1 FROM [FASTBOT].[dbo].[WhatsApp_BOT]c where c.Cell1 IS NOT NULL AND c.Cell1 LIKE '3%' AND c.STATO IS NULL")

risultati = cursor.fetchall()

driver = webdriver.Chrome(selenium_path)
driver.maximize_window()


for nums in risultati:
        try:
                nums = str(nums).replace('(','').replace("'", "").replace(",", "").replace(')', '')
                print(nums)
                driver.get("https://web.whatsapp.com/send?phone=+39" + str(nums))
                time.sleep(20)
                driver.find_element_by_xpath('//div[@class="p3_M1"]').click()
                time.sleep(1)
                driver.find_element_by_xpath('//div[@class="p3_M1"]').send_keys("PROMO LIMITED EDITION - FIBRA DI TIM FINO A 1 GIGA - 19,90€/MESE PER 6 MESI POI 24,90€/MESE, PER MAGGIORI INFORMAZIONI DIGITA     *SI*     per essere ricontattato da un nostro Operatore")
                time.sleep(1)
                driver.find_element_by_xpath('//button[@class="_4sWnG"]').click()
                time.sleep(4)
                aggiorna = cursor.execute("UPDATE [FASTBOT].[dbo].[WhatsApp_BOT] SET STATO = 'Spedito', CODBOT = '{1}' WHERE CELL1 = '{0}'".format(nums, codbot))
                cursor.commit()

        except Exception as e:
                print(e)
                aggiorna = cursor.execute("UPDATE [FASTBOT].[dbo].[WhatsApp_BOT] SET STATO = 'Non Trovato', CODBOT = '{1}' WHERE CELL1 = '{0}'".format(nums, codbot))
                cursor.commit()


