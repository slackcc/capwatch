import sqlite3
import argparse
from CapwatchData import CapwatchData


class CapwatchEmailList(object):

    def __init__(self, capwatch_data):
    
        self.db = capwatch_data.db

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
    parser = argparse.ArgumentParser(description='Generate Email List from CAPWatch data')
    parser.add_argument('--dir', type=str, help='Directorate')
    parser.add_argument('--asst', action='store_true', default=False, help="Include assistants")
    parser.add_argument('--unit', type=str, default="%", help="Specify a unit number, default is all units.")

    args = parser.parse_args()

    cw = CapwatchData()
    em = CapwatchEmailList(cw)
    email = em.select_directorate_email(args.dir, include_asst=args.asst, unit=args.unit)
    print(", ".join(email))