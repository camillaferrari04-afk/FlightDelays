from database.DB_connect import DBConnect
from model.airport import Airport


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * 
                    from airports a 
                    order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getairportsmin(minimo:int):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.*
                    FROM airports a, flights f
                    WHERE a.ID = f.ORIGIN_AIRPORT_ID OR a.ID = f.DESTINATION_AIRPORT_ID
                    GROUP BY a.ID
                    HAVING COUNT(DISTINCT f.AIRLINE_ID) >= %s
                    ORDER BY a.AIRPORT ASC"""

        cursor.execute(query, (minimo,))

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getedges(minimo:int):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT 
                        LEAST(f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) AS air1, 
                        GREATEST(f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) AS air2, 
                        COUNT(*) AS weight
                    from flights f
                    where f.ORIGIN_AIRPORT_ID in (SELECT a.ID 
                                    FROM airports a, flights f
                                    where a.ID = f.ORIGIN_AIRPORT_ID OR a.ID = f.DESTINATION_AIRPORT_ID
                                    GROUP BY a.ID
                                    HAVING COUNT(DISTINCT f.AIRLINE_ID) >= %s
                                    )
                        and f.DESTINATION_AIRPORT_ID in (SELECT a.ID 
                                    FROM airports a, flights f
                                    where a.ID = f.ORIGIN_AIRPORT_ID OR a.ID = f.DESTINATION_AIRPORT_ID
                                    GROUP BY a.ID
                                    HAVING COUNT(DISTINCT f.AIRLINE_ID) >= %s
                                    )
                    group by air1, air2 """

        cursor.execute(query, (minimo, minimo))

        for row in cursor:
            result.append({"air1": row["air1"], "air2": row["air2"], "weight": row["weight"]})

        cursor.close()
        conn.close()
        return result