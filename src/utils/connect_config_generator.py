class ConfigGenerator:
    """
    A helper class to generate configurations for source and sink databases
    """

    def __init__(self, *args, **kwargs):
        """
        kwargs
            :param: dict: credentials
        """
        self.type = kwargs.get("type")
        self.credentials = kwargs.get("credentials")

    def _unpack_credentials(
        self,
    ) -> dict:
        return {
            "database.hostname": self.credentials.get("host"),
            "database.port": self.credentials.get("port"),
            "database.user": self.credentials.get("user"),
            "database.password": self.credentials.get("password"),
        }
