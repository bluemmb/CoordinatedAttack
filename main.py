
"""
    Mohammad Eftekhari
"""

from random import randint
from math import inf
import logging
import matplotlib.pyplot as plt


class Message:
    messageID: int = 0

    def __init__(self, sender, receiver, level, val, key):
        Message.messageID = Message.messageID + 1
        self.messageID = Message.messageID
        self.sender = sender
        self.receiver = receiver
        self.level = level.copy()
        self.val = val.copy()
        self.key = None
        if not(key is None):
            self.key = key.copy()

    def print(self):
        logger.debug("")
        logger.debug("Message %d from %d to %d" % (self.messageID, self.sender, self.receiver))
        logger.debug("    Level=%s, Val=%s, Key=%s" % (self.level, self.val, self.key))

    def print_not_delivered(self):
        logger.debug("\n- Not Delivered : %d to %d" % (self.sender, self.receiver))


class Process:

    def __init__(self, n, r, pid, val, processes):
        """Initialize dog object."""
        self.n = n
        self.r = r
        self.pid = pid
        self.rounds = 0
        self.decision = -1
        self.key = None
        self.processes = processes
        self.messages = []

        self.val = [-1] * (n+1)
        self.val[pid] = val

        self.level = [-1] * (n+1)
        self.level[pid] = 0

    def rand(self):
        if self.pid == 1 and self.rounds == 0:
            self.key = [0] * (self.r+1)
            for i in range(1, self.r+1):
                self.key[i] = randint(1, i)

    def msgs(self):
        for i in range(1, self.n+1):
            if i != self.pid:
                message = Message(self.pid, i, self.level, self.val, self.key)
                self.processes[i].get_message(message)

    def get_message(self, message: Message):
        if randint(1, 100) > (100 - MESSAGE_DELIVERY_PERCENTAGE):
            message.print()
            self.messages.append(message)
        else:
            message.print_not_delivered()

    def trans(self):

        # update rounds
        self.rounds = self.rounds + 1

        # update key
        for msg in self.messages:
            if not(msg.key is None):
                self.key = msg.key

        # update val and level
        for msg in self.messages:
            for i in range(1, self.n+1):
                if i == self.pid:
                    continue
                if msg.val[i] != -1:
                    self.val[i] = msg.val[i]
                if msg.level[i] != self.level[i]:
                    self.level[i] = max(self.level[i], msg.level[i])
        self.messages.clear()

        # update my own level
        mn = inf
        for i in range(1, self.n+1):
            if i == self.pid:
                continue
            mn = min(mn, self.level[i]) + 1
        self.level[self.pid] = mn

        # is last round ?
        if self.rounds == self.r:
            self.decision = self.make_decision()

    def make_decision(self):
        agree = 1
        for i in range(1, self.n + 1):
            if self.val[i] != 1:
                agree = 0
                break

        if not(self.key is None) and self.level[self.pid] >= self.key[self.rounds] and agree:
            return 1
        else:
            return 0

    def print_decision(self):
        logger.debug("Process %d decided on : %d" % (self.pid, self.decision))

    def print_status(self):
        logger.debug("")
        logger.debug("Process %d status : " % self.pid)
        logger.debug("  MyLevel  = %s" % self.level[self.pid])
        logger.debug("    Level  = %s" % self.level)
        logger.debug("    Val    = %s" % self.val)
        logger.debug("    Key    = %s" % self.key)
        logger.debug("    Dec    = %s" % self.decision)
        logger.debug("    Rounds = %s" % self.rounds)


class Data:

    def __init__(self, n, r):
        self.n = n
        self.r = r
        self.d = [-1] * 101

    def saveplot(self):
        fig, ax = plt.subplots()
        ax.plot(range(0,101), self.d)
        ax.set(xlabel='delivery percent', ylabel='corrects',
               title="nodes = %d, rounds = %d" % (self.n, self.r))
        ax.grid()
        fig.savefig("plots/n%d-r%d.png" % (self.n, self.r))


def nameof(n, r):
    return "n%d-r%d" % (n, r)


def is_right(processes: [Process]):

    should_be = 1
    for i in range(1, processes.__len__()):
        if processes[i].val[i] == 0:
            should_be = 0
            break

    ok = 1
    for i in range(1, processes.__len__()):
        if processes[i].make_decision() != should_be:
            ok = 0
            break

    return ok


def main(n, r):
    global data

    # create processes
    processes = [None] * (n+1)
    for i in range(1, n+1):
        processes[i] = Process(n, r, i, 1, processes)
        processes[i].rand()

    # go for it !
    for round in range(1, r+1):
        logger.debug("\n\n--- Round %d" % round)
        for i in range(1, n+1):
            processes[i].msgs()
        for i in range(1, n+1):
            processes[i].trans()
        data[nameof(n,round)].d[MESSAGE_DELIVERY_PERCENTAGE] += is_right(processes)

    # print status of the processes
    for i in range(1, n+1):
        processes[i].print_status()

    # print decision of the process in one place
    for i in range(1, n+1):
        processes[i].print_decision()


# Initial Values
MESSAGE_DELIVERY_PERCENTAGE = -1

# Initialize logger class
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

n = 5
r = 20
data = {}
for j in range(1,r+1):
    data[nameof(n,j)] = Data(n, j)

for d in range(0, 101, 1):
    MESSAGE_DELIVERY_PERCENTAGE = d
    iteration = 1000
    for c in range(1, iteration+1):
        main(n, r)
    logger.info("d = %d" % d)

for key, value in data.items():
    value.saveplot()
