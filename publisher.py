import pika

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare an exchange
channel.exchange_declare(exchange='example_exchange', exchange_type='direct')

# Publish a message to the exchange
message = "Helloooo momo"
channel.basic_publish(exchange='example_exchange', routing_key='example_key', body=message)

print(" [x] Sent '%s'" % message)

# Close the connection
connection.close()