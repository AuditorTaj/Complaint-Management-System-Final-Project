from confluent_kafka import Producer

KAFKA_TOPIC = "complaints"
KAFKA_SERVER = "kafka:9092"

p = Producer({'bootstrap.servers': KAFKA_SERVER})

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_message(key, value):
    p.produce(KAFKA_TOPIC, key=key, value=value, callback=delivery_report)
    p.poll(0)

if __name__ == "__main__":
    produce_message("key1", "value1")
    p.flush()
