import pytest
from app.services.kafka_producer import get_kafka_producer

def test_kafka_producer_import():
    assert get_kafka_producer is not None
