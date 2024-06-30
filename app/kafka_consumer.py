from confluent_kafka import Consumer, KafkaError

KAFKA_TOPIC = "complaints"
KAFKA_SERVER = "kafka:9092"
GROUP_ID = "complaint_consumer_group"

c = Consumer({
    'bootstrap.servers': KAFKA_SERVER,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest'
})

c.subscribe([KAFKA_TOPIC])

def consume_messages():
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        print(f'Received message: {msg.value().decode("utf-8")}')
    
if __name__ == "__main__":
    consume_messages()
