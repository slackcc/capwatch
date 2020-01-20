# capwatch

This package provides a utility to download CAPWatch data and store it locally in an SQLite3 database file as well as a variety of utility classes to utilize the CAPWatch data when stored in the SQLite DB.

## Config

All of the CAPWatch utilities require configuration utilizing either a configuration file or environment variables. If both a configuration file and environment variables are present the environment variables will override the configuration file values.

By default the configuration file is stored relative to the application user's home directory in a directory called ".capwatch" and in a file called config.json (i.e. - ~/.capwatch/config.json). See config.sample.json in this package for an example file.

| Config File | Env Variable      | Sample Value                               |
| :---------- | :---------------- | :----------------------------------------- |
| base_url    | CAPWATCH_BASE_URL | "https://<URL_FROM_CW>/api/cw"             |
| token       | CAPWATCH_TOKEN    | "KSDn20sKSssl99JSJN3smaa29w="              |
| org_id      | CAPWATCH_ORG_ID   | "1234"                                     |
| db_file     | CAPWATCH_DB_FILE  | "/Users/jsmith/.capwatch/capwatch_mawg.db" |