import pygame
import sys


class Screen:
    def __init__(self, engine):
        self.engine = engine
        self.drawables = []
        self.views = []

        self.engine.set_current_screen(self)

    def run(self):
        while self.engine.running:
            self.engine.clock.tick(self.engine.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.engine.running = False

            self.updates(events)
            self.middleUpdates(events)
            self.endUpdates(events)

            self.draw()

        pygame.quit()
        sys.exit()

    def updates(self, events):
        self.engine.mouse.update(events)
        self.engine.keyboard.update()
        self.engine.UI.update()
        self.engine.timer_manager.update()

    def middleUpdates(self, events):
        pass

    def endUpdates(self, events):
        self.engine.camera.update()

    def init_UI(self):
        pass

    def draw(self):
        self.engine.screen.fill(self.engine.BACKGROUND_COLOR)
        self.engine.draw_manager.draw(self.engine.screen)
        pygame.display.flip()

    def start_screen(self, screen):
        screen_to_start = screen(self.engine)
        self.engine.screens.append(self)
        screen_to_start.run()

    def back_to_last_screen(self):
        screen_to_start = self.engine.screens.pop()
        self.engine.current_screen = screen_to_start
        self.engine.draw_manager.current_screen = screen_to_start
        self.engine.UI.current_screen = screen_to_start
        screen_to_start.run()
