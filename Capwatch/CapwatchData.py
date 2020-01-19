import sqlite3
from CapwatchConfig import CapwatchConfig

class CapwatchData(object):

    def __init__(self):
    
        self.config = CapwatchConfig()
        self.db = self.__create_connection__()


    def __create_connection__(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.config.db_file)
        except sqlite3.Error as e:
            print(e)
    
        return conn

    def select_directorate_email(self, area, unit="%", include_asst=False):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """

        if include_asst:
            asst = "%"
        else:
            asst = "0"
    
        email_addresses = []
        cur = self.db.cursor()

        # Get primary email addresses for all members in a particular
        # directorate
        cur.execute(f"""
            SELECT
                MbrContact.Contact as Contact
            FROM
                Member
                INNER JOIN DutyPosition ON Member.CAPID = DutyPosition.CAPID
                INNER JOIN MbrContact ON Member.CAPID = MbrContact.CAPID
            WHERE Member.Type IS "SENIOR"
                  AND DutyPosition.FunctArea IS "{area}"
                  AND MbrContact.Type IS "EMAIL"
                  AND MbrContact.Priority IS "PRIMARY"
                  AND Member.Unit LIKE "{unit}"
                  AND DutyPosition.Asst LIKE "{asst}"
            GROUP BY Member.CAPID;
        """)
    
        rows = cur.fetchall()
    
        for row in rows:
            email_addresses.append(row[0])

        return email_addresses

if __name__ == "__main__":
    cw = CapwatchData()
    email = cw.select_directorate_email("DC")
    print(email)