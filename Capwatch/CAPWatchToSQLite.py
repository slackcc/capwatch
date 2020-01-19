import sqlite3
import csv
import re
import os
import logging
from typing import List
from zipfile import ZipFile
import tempfile
from shutil import rmtree, copyfileobj
import urllib3
import certifi
from CapwatchConfig import CapwatchConfig

# Logger
log = logging.getLogger(__name__)
log.setLevel(os.environ.get("LOGLEVEL", "INFO"))

# Setup the HTTP retries
retry: urllib3.util.Retry = urllib3.util.Retry(read=3, backoff_factor=2,
                                               status_forcelist=[429, 503])

# Get an HTTP handler
http: urllib3.PoolManager = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

# Build regex pattern to recognize CAPWatch dates
pattern = re.compile("^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$")


class CAPWatchToSQLite(object):

    def __init__(self) -> None:
        """Constructor
        
        Arguments:
            directory {str} -- Directory where the CAPWatch files are stored
        """

        # Set the CAPWatch files directory
        self.directory = tempfile.mkdtemp()
        self.config = CapwatchConfig()

        log.debug(f"Temp Dir = {self.directory}")

        # Initialize list of CAPWatch files
        self.capwatch_files = []

    def get_capwatch_data(self, unit_only: int = 0) -> int:
        """[summary]
        
        Arguments:
            token {str} -- [description]
            org_id {str} -- [description]
        
        Keyword Arguments:
            unit_only {int} -- [description] (default: {0})
        
        Returns:
            int -- [description]
        """

        # Build the CAPWatch URL
        capwatch_url = f"{self.config.base_url}?ORGID={self.config.org_id}&unitOnly={unit_only}"

        # Setup the auth header
        headers = {
            "Authorization": f"Basic {self.config.token}"
        }

        # Get the CAPWatch data from NHQ
        with http.request(
            'GET',
            capwatch_url,
            headers=headers,
            preload_content=False) as resp, tempfile.NamedTemporaryFile(mode='wb', suffix=".zip", delete=False) as out_file:

                if resp.status == 200:
                    tempfile_name = out_file.name
                    copyfileobj(resp, out_file)
                else:
                    return resp.status

        # Unzip the zip file into a temp directory
        with ZipFile(tempfile_name, "r") as zip_obj:
                zip_obj.extractall(self.directory)

        # Delete the capwatch zip file
        os.unlink(tempfile_name)

        # Populate the CAPWatch files
        self.__get_files__()

        return resp.status
    
    def create_db(self) -> None:
        """[summary]
        
        Arguments:
            db_name {str} -- [description]
        """

        # Create a new SQLite3 DB file
        self.db = sqlite3.connect(self.config.db_file)

        # Set the cursor to the DB just created
        self.cursor = self.db.cursor()

        # Loop through the list of CAPWatch files
        for filename in self.capwatch_files:

            log.info(f"Creating table {filename.replace('.txt', '')}")

            # Create a table for each file
            self.__create_table__(filename)

        # Save the Database
        self.db.commit()

        # Delete the temporary directory
        rmtree(self.directory)

    def __table_fields__(self, headers: List[str]) -> str:
        """Generate the table fields to create the SQLite table with
        based on the header values in the CSV files. All fields will be
        inserted as Text fields
        
        Arguments:
            headers {List[str]} -- Array containing the header row column titles
        
        Returns:
            str -- String to insert into table creation command
        """

        # Initialize fields empty
        fields: str = ""

        # Loop through the header names from the CSV files
        for header in headers:

            # Build the field list out
            fields += f"{header} Text,"

        # Return the string to use for table creation, removing the last comma
        return fields.strip(",")


    def __get_files__(self) -> None:
        """[summary]
        
        Arguments:
            directory {str} -- [description]
        
        Returns:
            List[str] -- [description]
        """

        # Loop through files in directory
        for filename in os.listdir(self.directory):

            # Get the text files (which CAPWatch uses for CSV)
            if filename.endswith(".txt"):

                # Add the filename to the outgoing list
                self.capwatch_files.append(filename)

    def __parse_data__(self, data: str) -> str:
        """[summary]
        
        Arguments:
            data {str} -- [description]
        
        Returns:
            str -- [description]
        """

        data = data.strip("\"")

        if pattern.match(data):
            date_field = data.split("/")
            return "%d-%.2d-%.2d 00:00:00" % (
                int(date_field[2]),
                int(date_field[0]),
                int(date_field[1]))
        else:
            return data


    def __create_table__(self, filename: str) -> None:
        """[summary]
        
        Arguments:
            filename {str} -- [description]
        """

        # Open the CSV file
        with open(f'{self.directory}/{filename}', "r") as csv_file:

            # Read in the CSV file
            csv_reader = csv.reader(
                csv_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_ALL,
                skipinitialspace=True)

            # Get the header row
            headers = next(csv_reader)

            # Name the table in SQL the same as the base filename
            table_name = filename.replace(".txt", "")

            # Get the fields to create in SQLite format
            fields = self.__table_fields__(headers)

            # Build the table creation command
            create_table_cmd = f"CREATE TABLE {table_name} ({fields})"

            # Execute the table creation SQL command
            self.cursor.execute(create_table_cmd)

            # Loop through all of the rows in the CSV file
            for row in csv_reader:

                # Loop through the values in each row, with index, and
                # parse the data item to strip off extra quotes and to
                # convert dates into SQLite date format
                for index, item in enumerate(row, start=0):
                    row[index] = self.__parse_data__(item)

                # Here we are creating the right number of entry values
                # based on the number of columns in the original CSV file
                # and creating the insert command to insert in the new table
                insert_cmd = f'INSERT INTO {table_name} VALUES ({("?," * len(headers)).strip(",")})'

                # Execute the SQL Insert
                self.cursor.execute(insert_cmd, row)


if __name__ == "__main__":

    cw_to_db = CAPWatchToSQLite()
    cw_to_db.get_capwatch_data()
    cw_to_db.create_db()