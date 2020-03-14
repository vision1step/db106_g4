from confluent_kafka import Consumer, KafkaException, KafkaError
import sys

def error_cb(err):
    print('Error: %s' % err)

def try_decode_utf8(data):
    if data:
        return data.decode('utf-8')
    else:
        return None

def my_assign(consumer_instance, partitions):
    for p in partitions:
        p.offset = 0
    print('assign', partitions)
    consumer_instance.assign(partitions)

def print_commit_result(err, partitions):
    if err:
        print('# Failed to commit offsets: %s: %s' % (err, partitions))
    else:
        for p in partitions:
            print('# Committed offsets for: %s-%s {offset=%s}' % (p.topic, p.partition, p.offset))

if __name__ == '__main__':
    props = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'stock_tracker',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'auto.commit.interval.ms': 6000,
        'on_commit': print_commit_result,
        'error_cb': error_cb
    }
    consumer = Consumer(props)
    topicName = "stock"
    consumer.subscribe([topicName], on_assign=my_assign)
    count = 0
    try:
        while True:
            records = consumer.consume(num_messages=3, timeout=1.0)
            if records is None:
                continue
            for record in records:
                if record is None:
                    continue
                if record.error():
                    if record.error().code() == KafkaError._PARTITION_EOF:
                        sys.stderr.write('%% {} [{}] reached end at offset {} - {}\n'.format(record.topic(), record.partition(), record.offset()))
                    else:
                        raise KafkaException(record.error())
                else:
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    timestamp = record.timestamp()
                    msgKey = try_decode_utf8(record.key())
                    msgValue = try_decode_utf8(record.value())
                    print('%s-%d-%d : (%s , %s)' % (topic, partition, offset, msgKey, msgValue))
    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')
    except Exception as e:
        sys.stderr.write(e)
    finally:
        consumer.close()

