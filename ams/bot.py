class Bot(Loggable):
    name = 'Bot'
    def __init__(self, sender):
        self._sender = sender
    def home(self):
        self._sender.send('G28 XY')
