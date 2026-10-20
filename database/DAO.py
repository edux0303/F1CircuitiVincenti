from database.DB_connect import DBConnect
from model.driver import Driver
class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(anno1, anno2):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT d.driverId AS id, d.forename AS nome, d.surname AS cognome, "
                 "d.nationality AS nazionalita, COUNT(*) AS vittorie "
                 "FROM drivers d, results re, races ra "
                 "WHERE d.driverId = re.driverId AND re.raceId = ra.raceId "
                 "AND ra.year BETWEEN %s AND %s "
                 "AND re.position = 1 "
                 "GROUP BY d.driverId, d.forename, d.surname, d.nationality")

        cursor.execute(query, (anno1, anno2))
        for row in cursor:
            results.append(Driver(row["id"], row["nome"], row["cognome"],
                                  row["nazionalita"], row["vittorie"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getVittorieCircuiti(anno1, anno2):
        conn = DBConnect.get_connection()
        results = []
        if conn is None:
            return results

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT DISTINCT re.driverId AS idP, ra.circuitId AS idC "
                 "FROM results re, races ra "
                 "WHERE re.raceId = ra.raceId "
                 "AND re.position = 1 "
                 "AND ra.year BETWEEN %s AND %s")
        cursor.execute(query, (anno1, anno2))
        for row in cursor:
            results.append((row["idP"], row["idC"]))
        cursor.close()
        conn.close()
        return results




