from database.DB_connect import DBConnect
from model.fermata import Fermata
from model.connessione import Connessione
from model.linea import Linea


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query, ())

        for row in cursor:
            result.append(Fermata(row["id_fermata"], row["nome"], row["coordX"], row["coordY"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllLinee():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM linea"
        cursor.execute(query, ())

        for row in cursor:
            result.append(Linea(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdge(v1, v2):  # il metodo è statico quindi non ci vuole self
        # i due parametri saranno l'id della stazione di partenza e l'id della stazione di arrivo

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from connessione c where c.id_stazP = %s and c.id_stazA = %s"""

        cursor.execute(query, (v1.id_fermata, v2.id_fermata))

        for row in cursor:
            result.append(row)  # mi aspetto che o questo row sia vuoto (che il cursore stia iterando su una
            # tabella vuota) o che questo row sia una o più righe perché magari ci sono più archi tra quei due nodi.
            # In una prima fase voglio solo sapere se c'è un arco tra A e B, non quanti sono, per
            # questo metto tutto in result e poi mi vado a vedere la lunghezza di questo result
            # c

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdgesVicini(v1):  # solo un ingresso perché fisso solo il nodo source

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select * from connessione c where c.id_stazP = %s """
        cursor.execute(query, (v1.id_fermata,))

        for row in cursor:
            result.append(Connessione(row["id_connessione"], row["id_linea"], row["id_stazP"], row["id_stazA"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnessioni():

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select * from connessione c """
        cursor.execute(query, ())  # questo cursore sarà pieno perché prende tutte le connessioni

        for row in cursor:
            result.append(Connessione(row["id_connessione"], row["id_linea"], row["id_stazP"], row["id_stazA"]))

        cursor.close()
        conn.close()
        return result


