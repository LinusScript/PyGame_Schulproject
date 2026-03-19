

import pygame


class GameOverScreen:
    def __init__(self, screen: pygame.Surface, title: str = "Pac-Man"):
        self.screen = screen
        self.title = title
        self.clock = pygame.time.Clock()
        self.running = True
        self.selected_index = 0
        self.options = ["Nochmal spielen", "Hauptmenü", "Beenden"]

        self.bg_color = (0, 0, 0)
        self.title_color = (255, 60, 60)
        self.text_color = (220, 220, 220)
        self.selected_color = (255, 255, 0)
        self.help_color = (160, 160, 160)
        self.score_color = (0, 200, 255)

        self.title_font = pygame.font.Font(None, 74)
        self.option_font = pygame.font.Font(None, 42)
        self.help_font = pygame.font.Font(None, 28)
        self.score_font = pygame.font.Font(None, 34)

    def move_up(self) -> None:
        self.selected_index = (self.selected_index - 1) % len(self.options)

    def move_down(self) -> None:
        self.selected_index = (self.selected_index + 1) % len(self.options)

    def get_selected_action(self) -> str:
        if self.selected_index == 0:
            return "restart"
        if self.selected_index == 1:
            return "menu"
        return "quit"

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.QUIT:
            self.running = False
            return "quit"

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.move_up()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.move_down()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.get_selected_action()
            elif event.key == pygame.K_ESCAPE:
                return "menu"

        return None

    def draw(self, score: int = 0, message: str = "Game Over") -> None:
        self.screen.fill(self.bg_color)
        width, height = self.screen.get_size()

        title_surface = self.title_font.render(message, True, self.title_color)
        title_rect = title_surface.get_rect(center=(width // 2, 140))
        self.screen.blit(title_surface, title_rect)

        subtitle_surface = self.help_font.render(self.title, True, self.help_color)
        subtitle_rect = subtitle_surface.get_rect(center=(width // 2, 190))
        self.screen.blit(subtitle_surface, subtitle_rect)

        score_surface = self.score_font.render(f"Punktestand: {score}", True, self.score_color)
        score_rect = score_surface.get_rect(center=(width // 2, 250))
        self.screen.blit(score_surface, score_rect)

        start_y = 340
        spacing = 65

        for index, option in enumerate(self.options):
            is_selected = index == self.selected_index
            color = self.selected_color if is_selected else self.text_color
            prefix = "> " if is_selected else "  "
            option_surface = self.option_font.render(f"{prefix}{option}", True, color)
            option_rect = option_surface.get_rect(center=(width // 2, start_y + index * spacing))
            self.screen.blit(option_surface, option_rect)

        help_surface = self.help_font.render(
            "Pfeiltasten/W/S = Auswahl | Enter = Bestätigen | Esc = Menü",
            True,
            self.help_color,
        )
        help_rect = help_surface.get_rect(center=(width // 2, height - 70))
        self.screen.blit(help_surface, help_rect)

        pygame.display.flip()

    def run(self, score: int = 0, message: str = "Game Over") -> str:
        self.running = True
        self.selected_index = 0

        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                action = self.handle_event(event)
                if action is not None:
                    return action

            self.draw(score=score, message=message)

        return "quit"