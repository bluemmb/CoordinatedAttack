
"""
    Mohammad Eftekhari
"""

from random import randint
from math import inf


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


class Process:

    def __init__(self, n, r, pid, val, processes):
        """Initialize dog object."""
        self.n = n
        self.r = r
        self.pid = pid
        self.rounds = 0
        self.decision = -1
        self.key = -1
        self.processes = processes
        self.messages = []

        self.val = [-1] * (n+1)
        self.val[pid] = val

        self.level = [-1] * (n+1)
        self.level[pid] = 0

    def rand(self):
        if self.pid == 1 and self.rounds == 0:
            self.key = randint(1, self.r)

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
            print("\n- Not Delivered : %d to %d" % (message.sender, message.receiver))
            global MessagesNotDelivered
            MessagesNotDelivered = MessagesNotDelivered + 1

    def trans(self):

        # update rounds
        self.rounds = self.rounds + 1

        # update key
        for msg in self.messages:
            if msg.key != -1:
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

            agree = 1
            for i in range(1, self.n+1):
                if self.val[i] != 1:
                    agree = 0
                    break

            if self.key != -1 and self.level[self.pid] >= self.key and agree:
                self.decision = 1
            else:
                self.decision = 0

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


def is_right(processes: [Process]):

    should_be = 1
    for i in range(1, processes.__len__()):
        if processes[i].val[i] == 0:
            should_be = 0
            break

    it_is = 1
    for i in range(1, processes.__len__()):
        if processes[i].decision == 0:
            it_is = 0
            break

    return should_be == it_is


def main(n, r):

    # create processes
    processes = [None] * (n+1)
    for i in range(1, n+1):
        processes[i] = Process(n, r, i, 1, processes)
        processes[i].rand()

    # go for it !
    for round in range(1, r+1):
        print("\n\n--- Round %d" % round)
        for i in range(1, n+1):
            processes[i].msgs()
        for i in range(1, n+1):
            processes[i].trans()

    # print status of the processes
    for i in range(1, n+1):
        processes[i].print_status()

    # print decision of the process in one place
    print()
    for i in range(1, n+1):
        processes[i].print_decision()

    print("\nMessagesNotDelivered : %d out of %d" % (MessagesNotDelivered, r*n*(n-1)))

    return is_right(processes)


MESSAGE_DELIVERY_PERCENTAGE = 95
MessagesNotDelivered = 0

n = 4
for r in range(1,2):
    for d in range(80,101,5):
        MESSAGE_DELIVERY_PERCENTAGE = d
        MessagesNotDelivered = 0
        ans = main(n, r)
        print("r = %d, d = %d, ans = %d" % (r, d, ans))


