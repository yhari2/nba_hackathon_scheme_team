class Player:

    def __init__(self, pid, status=False, diff=0):
        self.pid = pid
        self.status = status
        self.diff = diff

    def __str__(self):
        return "{},{}".format(self.pid, self.diff)

    def __hash__(self):
        return hash(self.pid)

    def __eq__(self, other):
        return self.pid == other.pid

    def sub(self):
        self.status = not self.status

    def score(self, points):
        self.diff = self.diff + points
