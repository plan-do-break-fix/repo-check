#!/bin/python3
import pika


class Interface:

    def __init__(self, host, user, password):
        self.host, self.user, self.password = host, user, password

    def enqueue(self, message, qname) -> bool:
        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=qname,
                body=message
            )
            return True
        except pika.exception.StreamLostError:
            self.connect()
            self.enqueue(message, qname)

    def dequeue(self, qname) -> str:
        self.connect()
        method, header, body = self.channel.basic_get(queue=qname)
        if not body:
            self.connection.close
            return False
        else:
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
            self.connection.close
            return body.decode()
        
    def message_count(self, qname) -> int:
        self.connect()
        response = self.channel.queue_declare(qname, passive=True)
        return response.method.message_count

    def connect(self) -> True:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                credentials=pika.credentials.PlainCredentials(
                    self.user,
                    self.password
                )
            )
        )
        self.channel = self.connection.channel()
        return True
