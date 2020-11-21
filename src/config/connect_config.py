class ConnectConfig(object):
    kafka_connect_host = "localhost"
    kafka_connect_port = 8083
    # kafka_connect_url = "localhost:8083"
    kafka_connect_url = f"http://:{kafka_connect_host}:{kafka_connect_port}/"
    topic_prefix = "playground"

    file_request_payload = {
        "connector.class": "io.streamthoughts.kafka.connect.filepulse.source.FilePulseSourceConnector",
        ## "fs.scan.directory.path": < Update this before calling add >
        "skip.headers": 1,  ## For now staying with clean data, first row is header is assumed
        "task.reader.class": "io.streamthoughts.kafka.connect.filepulse.reader.RowFileInputReader",
        # "topic":< Update the topic you want the write data into >,
        "internal.kafka.reporter.bootstrap.servers": "localhost:9092",
        "internal.kafka.reporter.topic": "connect-file-pulse-status",
        "fs.cleanup.policy.class": "io.streamthoughts.kafka.connect.filepulse.clean.DeleteCleanupPolicy",
        "tasks.max": 1,
    }
