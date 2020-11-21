from src.config.connect_config import ConnectConfig
import requests
import json


class ConnectionHandler:
    def __init__(self, *args, **kwargs):
        self.connect_base_url = ConnectConfig.kafka_connect_url
        self.con

    def add_connection(
        self,
    ):

        pass

    def list_connections(
        self,
    ):
        pass

    def _get_connection_status(self, conn_id: str = "") -> dict or bool:
        status_url = f"{self.connect_base_url}/{conn_id}/status"
        response = requests.get(
            status_url,
        )
        if response.status_code == 200:
            return response.json
        else:
            return False

    def _check_if_exists(self, conn_id: str = "") -> (bool, dict):
        status = self._get_connection_status(conn_id=conn_id)
        if status:
            return (True, status)
        else:
            return (False, {})
