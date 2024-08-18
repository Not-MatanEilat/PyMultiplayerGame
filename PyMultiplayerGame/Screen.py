import pygame
import sys


class Screen:
    def __init__(self, engine):
        self.engine = engine
        self.views = []

        self.screen_to_change = None
        self.running = True

    def run(self):

        self.on_create()

        while self.running:
            self.engine.clock.tick(self.engine.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.engine.running = False

            self.updates(events)
            self.middleUpdates(events)
            self.endUpdates(events)

            self.draw_screen()

            self.check_for_screen_change()
            self.check_for_game_finish()

        # on screen finish
        self.engine.screens.pop()
        self.dispose()

    def on_create(self):
        pass

    def check_for_game_finish(self):
        if not self.engine.running:
            self.exit_game()

    def exit_game(self):
        pygame.quit()
        exit(0)

    def updates(self, events):
        self.engine.mouse.update(events)
        self.engine.keyboard.update()
        for view in self.views:
            view.update(self.engine.mouse, self.engine.keyboard)
        self.engine.timer_manager.update()

    def middleUpdates(self, events):
        pass

    def endUpdates(self, events):
        self.engine.camera.update()

    def init_UI(self):
        pass

    def draw_screen(self):
        self.draw()
        pygame.display.flip()

    def draw(self):
        self.engine.screen.fill(self.engine.BACKGROUND_COLOR)
        for view in self.views:
            view.draw(self.engine.screen, self.engine.camera)
    def add_view(self, view):
        self.views.append(view)

    def on_packet_received(self, response_code, data):
        print("Packet received with code: " + str(response_code) + " and data: " + str(data))

    def on_communicator_error(self, error):
        print("Communicator error: " + str(error))

    def check_for_screen_change(self):
        if self.screen_to_change is not None:

            self.engine.current_screen = self.screen_to_change
            self.screen_to_change.run()

            self.engine.current_screen = self
            self.screen_to_change = None

    def start_screen(self, screen_to_start):
        self.engine.screens.append(screen_to_start)
        self.screen_to_change = screen_to_start

    def back_to_last_screen(self):

        self.running = False

    def dispose(self):
        pass
