import os
import json
import logging
from pathlib import Path

# Logger
log = logging.getLogger(__name__)
log.setLevel(os.environ.get("LOGLEVEL", "INFO"))

class CapwatchConfig(object):

    def __init__(self, config_file=f"{Path.home()}/.capwatch/config.json"):
        """[summary]
        
        Keyword Arguments:
            config_file {[type]} -- [description] (default: {f"{Path.home()}/.capwatch/config.json"})
        """

        self.config_file = config_file

        self.base_url = None
        self.token = None
        self.org_id = None
        self.db_file = None

        # Read config file first
        self.__read_config_file__()

        # Read environment variables next (these will override
        # the config file if present)
        self.__read_env__()

    def __read_config_file__(self) -> None:
        """[summary]
        """

        try:
            with open(self.config_file, "rb") as cf:

                config = json.load(cf)

                self.base_url = config.get("base_url", "")
                self.token = config.get("token", "")
                self.org_id = config.get("org_id", "")
                self.db_file = config.get("db_file", "")

                log.info(f"Successfully read {self.config_file}")

        except:
            log.warn("Could not open config file.")
            pass
    
    def __read_env__(self) -> None:
        """Check to see if the environment variables exist and set
        the class variables if they do
        """

        if os.environ.get("CAPWATCH_BASE_URL"):
            self.base_url = os.environ.get("CAPWATCH_BASE_URL")

        if os.environ.get("CAPWATCH_TOKEN"):
            self.token = os.environ.get("CAPWATCH_TOKEN")

        if os.environ.get("CAPWATCH_ORG_ID"):
            self.org_id = os.environ.get("CAPWATCH_ORG_ID")

        if os.environ.get("CAPWATCH_DB_FILE"):
            self.db_file = os.environ.get("CAPWATCH_DB_FILE")

    def validate(self) -> bool:
        """[summary]
        
        Returns:
            bool -- [description]
        """

        self.errors = []

        if self.base_url == None:
            self.errors.append("Base URL")

        if self.token == None:
            self.errors.append("Token")

        if self.org_id == None:
            self.errors.append("Org ID")

        if self.db_file == None:
            self.errors.append("DB File")

        if len(self.errors) != 0:
            log.error(f"CAPWatch Config items missing: {', '.join(self.errors)}")
            return False
        
        return True
