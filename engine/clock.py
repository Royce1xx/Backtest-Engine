# backtestr/engine/clock.py
class Clock:
    def __init__(self, timeline):
        self.timeline = timeline
        self.i = 0

    def has_next(self):
        return self.i < len(self.timeline)

    def next(self):
        ts = self.timeline[self.i]
        self.i += 1
        return ts
