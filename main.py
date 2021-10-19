import configparser
import time
import random
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from Database import Database, Queryes

""""Config configparser"""
config = configparser.RawConfigParser()
config.read('config.properties')

"""Config and config"""
selenium_path = config.get('Selenium', 'path')
testo = config.get('OFFERTA', 'testo')
type = config.get('MODE', 'type')
codbot = config.get('CODBOT', 'cod')

class Site():

    def __init__(self):
        self.selenium_path = config.get('Selenium', 'path')
        self.driver = webdriver.Chrome(selenium_path)
        self.testo = testo
        self.type = type
        self.codbot = codbot

    def login_toWhatsappWeb(self):

        self.driver.maximize_window()
        self.driver.get('https://web.whatsapp.com/')
        print("Hai 15 sec per scannerizzare il QR CODE")
        time.sleep(15)

    def close_driver(self):
        self.driver.quit()

    def check_if_logged(self):

        if 'Mantieni il telefono connesso' in self.driver.page_source:

            print("Ok sei connesso. Comincio a scassare la minchia.")
            logged = True
        else:
            logged = False

        return logged

    def select_numbers_and_prenoteTHEM(self):

        numbers = Database.dbQuery(self,Queryes.select_numbers(self,self.codbot))
        if numbers is None:
            Database.dbQuery_update(self, Queryes.prenote250_numbers(self,self.codbot))
            print("Prenotato 250 numeri.")
            numbers = Database.dbQuery(self, Queryes.select_numbers(self,self.codbot))
        return numbers

    def message_sender(self, number):
        try:
            text = Site.random_text(self)
            # self.driver.get('https://api.whatsapp.com/send/?phone=%2B39{0}&text={1}&app_absent=0'.format(number, text))
            time.sleep(2)
            self.driver.get("https://web.whatsapp.com/send?phone=+39" + str(number))
            time.sleep(20)
            self.driver.find_element_by_xpath('//div[@class="p3_M1"]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//div[@class="p3_M1"]').send_keys(text)
            time.sleep(1)
            self.driver.find_element_by_xpath('//button[@class="_4sWnG"]').click()
            time.sleep(4)
            try:
                if 'non trovato' in self.driver.page_source:
                    print(f"Numero : {number} non trovato .. Update state _NOT-FOUND")
                    Database.dbQuery_update(self, Queryes.update_state_no(self,number,self.codbot, self.type))
                    time.sleep(2)
                elif 'tentativo' in self.driver.page_source:
                    print(f"Errore {number} nel tentativo di invio .. \n Update state _ERROR")
                    Database.dbQuery_update(self, Queryes.update_state_error(self, number, self.codbot, self.type))
                    time.sleep(30)
                else:
                    print(f"Update  : {number} stateo _OK \n Procedo.")
                    Database.dbQuery_update(self, Queryes.update_state_ok(self, number, self.codbot, self.type))

            except Exception as e:
                print(str(e))
                print("Errore in fase message sender")

        except Exception as e:
            print("Errore ad inizio message sender")
            time.sleep(2)

    def random_text(self):
        lista_saluti = ['Salve', ' Ciao', 'Gentile Cliente']
        random_n = random.randint(0,2)
        testo =f'{lista_saluti[random_n]}, {self.testo}  **'

        return testo

    def message_sender_rompi(self, number):
        try:

            text = Site.random_text_rompi(self)
            # self.driver.get('https://api.whatsapp.com/send/?phone=%2B39{0}&text={1}&app_absent=0'.format(number, text))
            time.sleep(2)
            self.driver.get("https://web.whatsapp.com/send?phone=+39" + str(number))
            time.sleep(20)
            self.driver.find_element_by_xpath('//div[@class="p3_M1"]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('//div[@class="p3_M1"]').send_keys(text)
            time.sleep(1)
            self.driver.find_element_by_xpath('//button[@class="_4sWnG"]').click()
            time.sleep(4)
        except Exception as e:
            print(e)

    def random_text_rompi(self):
        lista_saluti = ['YOOO', ' Ciao', 'Fratm', 'Lo zio ture ti ringrazia', 'Hai visto a melo?','Forse si','Potrebbe','Può darsi']
        random_n = random.randint(0,7)
        testo =str(lista_saluti[random_n])

        return testo