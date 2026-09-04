import json

from kafka import KafkaProducer


KAFKA_BOOTSTRAP_SERVERS = "127.0.0.1:9092"
TRANSACTION_TOPIC = "transaction.created"


def get_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        api_version=(4, 0, 0),
        request_timeout_ms=3000,
        api_version_auto_timeout_ms=3000,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )


def publish_transaction_event(transaction):
    producer = get_producer()

    try:
        producer.send(
            TRANSACTION_TOPIC,
            value=transaction,
        )

        producer.flush()

    finally:
        producer.close()