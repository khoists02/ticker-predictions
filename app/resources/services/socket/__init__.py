from flask_socketio import namespace, emit


class TicketCurrentPriceSocket(namespace):
    def on_connect(self):
        print("connect")

    def on_disconnect(self):
        print("disconnect")

    def send_current(self, data):
        emit('ticket', data)
