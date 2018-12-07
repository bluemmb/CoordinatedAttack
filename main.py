
from random import randint
from math import inf
from queue import Queue


class Message:
    messageID: int = 0

    def __init__(self, sender, receiver, level, val, key):
        Message.messageID = Message.messageID + 1
        self.messageID = Message.messageID
        self.sender = sender
        self.receiver = receiver
        self.level = level.copy()
        self.val = val.copy()
        self.key = key

    def print(self):
        print()
        print("Message %d from %d to %d" % (self.messageID, self.sender, self.receiver))
        print("    Level=%s, Val=%s, Key=%d" % (self.level, self.val, self.key))


class Messenger:

    def __init__(self, processes):
        self.processes = processes
        self.q = Queue()

    def send_message(self, message: Message):
        self.q.put(message)

    def has_message(self):
        return not self.q.empty()

    def deliver(self):
        if not self.has_message():
            return
        message = self.q.get()
        receiver = message.receiver
        message.print()
        self.processes[receiver].trans(message)


class Process:

    def __init__(self, n, r, pid, decision, messenger):
        """Initialize dog object."""
        self.n = n
        self.r = r
        self.pid = pid
        self.rounds = 0
        self.decision = -1
        self.key = -1
        self.messenger = messenger

        self.val = [-1] * (n+1)
        self.val[pid] = decision

        self.level = [-1] * (n+1)
        self.level[pid] = 0

    def rand(self):
        if self.pid == 1 and self.rounds == 0:
            self.key = randint(1, self.r)

    def msgs(self):
        for i in range(1, self.n+1):
            if i != self.pid:
                message = Message(self.pid, i, self.level, self.val, self.key)
                self.messenger.send_message(message)

    def trans(self, message: Message):

        # ignore extra messages
        if self.rounds == self.r:
            print("!IGNORED")
            return

        # update rounds
        self.rounds = self.rounds + 1

        # update key
        if message.key != -1:
            self.key = message.key

        # update val and level
        mn = inf
        for i in range(1, self.n+1):
            if i == self.pid:
                continue
            if message.val[i] != -1:
                self.val[i] = message.val[i]
            if message.level[i] != self.level[i]:
                self.level[i] = message.level[i]
            mn = min( mn , message.level[i] ) + 1

        self.level[self.pid] = mn

        # is last round ?
        if self.rounds == self.r:

            agree = 1
            for i in range(1, self.n+1):
                if self.val[i] != 1:
                    agree = 0
                    break

            if self.key != -1 and self.level[self.pid] >= self.key and agree:
                self.decision = 1
            else:
                self.decision = 0

        elif self.rounds < self.r:
            self.msgs()

    def print_decision(self):
        print("Process %d decided on : %d" % (self.pid, self.decision))

    def print_status(self):
        print()
        print("Process %d status : " % self.pid)
        print("  MyLevel  = %s" % self.level[self.pid])
        print("    Level  = %s" % self.level)
        print("    Val    = %s" % self.val)
        print("    Key    = %s" % self.key)
        print("    Dec    = %s" % self.decision)
        print("    Rounds = %s" % self.rounds)


def main(n, r):

    # create processes
    processes = [None] * (n+1)
    messenger = Messenger(processes)
    for i in range(1, n+1):
        processes[i] = Process(n, r, i, 1, messenger)
        processes[i].rand()

    # initial message queue
    for i in range(1, n+1):
        processes[i].msgs()

    # go for it !
    while messenger.has_message():
        messenger.deliver()

    # print status of the processes
    for i in range(1, n+1):
        processes[i].print_status()

    # print decision of the process in one place
    print()
    for i in range(1, n+1):
        processes[i].print_decision()



main(3, 25)

