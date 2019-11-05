class Room():
    
    def __init__(self, queue, auth_token):
        self.queue = []
        self.token = auth_token
    
    def updateQueue(self, queue):
        self.queue = queue
    
    def getQueue(self):
        return self.queue

    def addToQueue(self, song):
        self.queue.append(song)