import pyodbc
import time
import configparser

"""DB CONNECTION"""
STRING_DBCONN = ('Driver={SQL Server};'
                 'Server=192.168.0.190;'
                 'Database=ENERGIA;'
                 'Uid=icox;'
                 'Pwd=iAmByou#2014')

""""Config configparser"""
config = configparser.RawConfigParser()
config.read('config.properties')

"""Credentials"""
type = config.get('MODE', 'type')
codbot = config.get('CODBOT', 'cod')


class Database():
    def dbQuery(self, query):  # -- PER LE SELECT
        conn = pyodbc.connect(STRING_DBCONN)
        self.cursor = conn.cursor()
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.cursor.close()
        return result

    def dbQuery_update(self, query):  # -- PER UPDATE
        conn = pyodbc.connect(STRING_DBCONN)
        self.cursor = conn.cursor()
        self.cursor.execute(query)
        self.cursor.commit()
        self.cursor.close()

    def work_on_db(self, dict):
        pass


class Queryes():

    def prenote250_numbers(self, codbot):
        query = """ UPDATE TOP(500) W SET CODBOT = '{1}'
                    FROM [FASTBOT].[dbo].[WhatsApp_BOT_TEST] W
                    WHERE W.STATO IS NUL AND W.CODBOT is null """.format(codbot)
        return query

    def select_numbers(self, codbot):
        query = """ SELECT CELL1
                    FROM [FASTBOT].[dbo].[WhatsApp_BOT_TEST] W
                    WHERE W.STATO IS NULL  AND W.CODBOT = '{0}'""".format(codbot)
        return query

    def update_state_ok(self, number, codbot, type):
        query = """UPDATE [FASTBOT].[dbo].[WhatsApp_BOT_TEST] SET STATO = 'Spedito', CODBOT = '{1}', LAST_UPDATE=GETDATE(), TYPE='{2}'WHERE CELL1 = '{0}'".format(number, codbot, type)"""
        return query

    def update_state_no(self, number, codbot, type):
        query = """UPDATE [FASTBOT].[dbo].[WhatsApp_BOT_TEST] SET STATO = 'Non trovato', CODBOT = '{1}',LAST_UPDATE=GETDATE(), TYPE='{2}' WHERE CELL1 = '{0}'".format(number, codbot, type)"""
        return query

    def update_state_error(self, number, codbot, type):
        query = """UPDATE [FASTBOT].[dbo].[WhatsApp_BOT_TEST] SET STATO = 'Errore', CODBOT = '{1}',LAST_UPDATE=GETDATE(), TYPE='{2}'WHERE CELL1 = '{0}'".format(number, codbot, type)"""
        return query
