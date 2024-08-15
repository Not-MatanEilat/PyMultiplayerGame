import pygame

class TimerManager:
    instance = None
    def __init__(self):
        self.timers = []
        TimerManager.instance = self


    @staticmethod
    def get_instance():
        if TimerManager.instance is None:
            TimerManager()
        return TimerManager.instance

    def update(self):
        for timer in self.timers:
            timer.update()

class Timer:
    def __init__(self):
        self.paused = False
        self.started = False

        self.start_ticks = 0
        self.pause_ticks = 0

    def start(self):
        self.started = True
        self.start_ticks = pygame.time.get_ticks()

    def stop(self):
        self.started = False
        self.pause_ticks = 0

    def pause(self):
        self.paused = True
        self.pause_ticks = pygame.time.get_ticks()

    def unpause(self):
        self.paused = False
        self.start_ticks += pygame.time.get_ticks() - self.pause_ticks
        self.pause_ticks = 0

    def get_ticks(self):
        if self.started:
            if self.paused:
                return self.pause_ticks - self.start_ticks
            else:
                return pygame.time.get_ticks() - self.start_ticks
        return 0

    def is_started(self):
        return self.started

    def is_paused(self):
        return self.paused

    def delete(self):
        TimerManager.get_instance().timers.remove(self)


class CountdownTimer(Timer):
    def __init__(self, time, repeat=False):
        super().__init__()
        self.time = time
        self.repeat = repeat

        self.on_finish = None
        TimerManager.get_instance().timers.append(self)

    def update(self):
        if self.is_started():
            if self.get_ticks() / 1000 >= self.time:

                if self.repeat:
                    self.start()
                else:
                    self.stop()

                if self.on_finish is not None:
                    self.on_finish()

    def get_time_is_left(self):
        return self.time - self.get_ticks() / 1000

