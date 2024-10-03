import pika

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue (the queue should match the one to which the exchange routes messages)
channel.queue_declare(queue='example_queue')

# Function to handle incoming messages
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# Bind the queue to the exchange
channel.queue_bind(exchange='example_exchange', queue='example_queue', routing_key='example_key')

# Tell RabbitMQ to deliver messages from the queue
channel.basic_consume(queue='example_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()