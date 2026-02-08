from app.services.kafka_consumer import KafkaTaskConsumer

def test_kafka_consumer_import():
    assert KafkaTaskConsumer is not None
