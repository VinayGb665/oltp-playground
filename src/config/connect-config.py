class ConnectConfig(object):
    kafka_connect_host = "mysql.db.test.synctactic.ai"
    kafka_connect_port = 8083
    kafka_connect_url = f"http://:{kafka_connect_host}:{kafka_connect_port}/"
    topic_prefix = 'playground'