import random
from main import Site


class Start():

    def __init__(self):

        try:

            Site.__init__(self)
            Site.login_toWhatsappWeb(self)
            logged = Site.check_if_logged(self)

            if logged is True:
                # while logged is True:
                    numbers = Site.select_numbers_and_prenoteTHEM(self)
                    count = 0
                    print("Started.")
                    if numbers is None:
                        print("Numeri finiti!!!!!")
                        input("Premi un stato per chiudere..")
                        # break
                    else:
                        for num in numbers:
                            Site.message_sender(self, num)
                            count = count+1
                            if count == 20:
                                print("Parlo con gli con uno dei miei amici BOT..")
                                rompi_coglion_list = ['3332860407','3311554064','3311554065','3339479179']
                                Site.message_sender(self, rompi_coglion_list[random.randint(0,3)])
                                count = 0
                    # print("Prendo altri numeri..")
                    Site.close_driver(self)
                    input("FINE DI 250 ROMPI COGLIONI. PREMI UN TASTO PER CHIUDERE..")

            else:
                input("Non sei riuscito a scannerizzare in tempo il QR CODE \n Premi un tasto per chiudere.")

        except Exception as e:
            print(str(e))
            input("Errore... premi un tasto per chiudere.")


Start()
