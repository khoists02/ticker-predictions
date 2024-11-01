"""
Prediction System power by Khoi.le
"""
from flask_socketio import namespace, emit


class TicketCurrentPriceSocket(namespace):
    @staticmethod
    def on_connect():
        print("connect")

    @staticmethod
    def on_disconnect(self):
        print("disconnect")

    @staticmethod
    def send_current(self, data):
        emit('ticket', data)
