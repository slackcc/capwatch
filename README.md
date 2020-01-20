# capwatch

This package provides a utility to download CAPWatch data and store it locally in an SQLite3 database file as well as a variety of utility classes to utilize the CAPWatch data when stored in the SQLite DB.

## Installation

## Config

All of the CAPWatch utilities require configuration utilizing either a configuration file or environment variables. If both a configuration file and environment variables are present the environment variables will override the configuration file values.

By default the configuration file is stored relative to the application user's home directory in a directory called ".capwatch" and in a file called config.json (i.e. - ~/.capwatch/config.json). See config.sample.json in this package for an example file. See table below for config and corresponding environment variable names and sample values.


| Config File | Env Variable      | Sample Value                               |
| :---------- | :---------------- | :----------------------------------------- |
| base_url    | CAPWATCH_BASE_URL | "https://<URL_FROM_CW>/api/cw"             |
| token       | CAPWATCH_TOKEN    | "KSDn20sKSssl99JSJN3smaa29w="              |
| org_id      | CAPWATCH_ORG_ID   | "1234"                                     |
| db_file     | CAPWATCH_DB_FILE  | "/Users/jsmith/.capwatch/capwatch_mawg.db" |

## Create SQLite Database

After setting up the configuration file you can run the CapwatchToSQLite program to populate your local SQLite database filled with CAPWatch data. To run the application change to the directory where you downloaded the CAPWatch utilities (this git repo) and run the following (using Python 3.6 or above):

    cd ./Capwatch
    python CapwatchToSQLite.py
