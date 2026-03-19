import pygame

from src.level import Level
from src.states.gameover import GameOverScreen


class Game:
    def __init__(self, screen: pygame.Surface | None = None):
        if not pygame.get_init():
            pygame.init()

        self.level = Level()
        self.screen = screen or pygame.display.set_mode(self.level.pixel_size)
        pygame.display.set_caption("Pac-Man")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 42)

        self.player_speed = 150
        self.player_radius = max(8, self.level.tile // 3)
        self.ghost_radius = max(8, self.level.tile // 3)

        self.running = True
        self.show_grid = False
        self.show_entities = True
        self.score = 0
        self.lives = 3

        self._init_world_state()

    def _init_world_state(self) -> None:
        px, py = self.level.grid_to_pixel_center(self.level.spawn_player)
        self.player_pos = pygame.Vector2(px, py)
        self.ghost_positions = [
            pygame.Vector2(*self.level.grid_to_pixel_center(ghost_pos))
            for ghost_pos in self.level.spawn_ghosts
        ]

    def reset(self) -> None:
        self.level = Level()
        self.running = True
        self.show_grid = False
        self.show_entities = True
        self.score = 0
        self.lives = 3
        self._init_world_state()

    def draw_text(self, text: str, x: int, y: int, color: tuple[int, int, int] = (255, 255, 255)) -> None:
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def draw_entities(self) -> None:
        pygame.draw.circle(
            self.screen,
            (255, 255, 0),
            (int(self.player_pos.x), int(self.player_pos.y)),
            self.player_radius,
        )

        ghost_colors = [
            (255, 0, 0),
            (255, 105, 180),
            (0, 255, 255),
            (255, 165, 0),
        ]

        for index, ghost_pos in enumerate(self.ghost_positions):
            color = ghost_colors[index % len(ghost_colors)]
            pygame.draw.circle(
                self.screen,
                color,
                (int(ghost_pos.x), int(ghost_pos.y)),
                self.ghost_radius,
            )

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.QUIT:
            self.running = False
            return "quit"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                return "menu"
            if event.key == pygame.K_g:
                self.show_grid = not self.show_grid
            if event.key == pygame.K_e:
                self.show_entities = not self.show_entities
            if event.key == pygame.K_r:
                return "restart"
            if event.key == pygame.K_k:
                return "gameover"

        return None

    def move_player(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1

        if direction.length_squared() == 0:
            return

        direction = direction.normalize()
        next_pos = self.player_pos + direction * self.player_speed * dt
        next_rect = pygame.Rect(0, 0, self.player_radius * 2, self.player_radius * 2)
        next_rect.center = (round(next_pos.x), round(next_pos.y))

        if not self.level.rect_collides_walls(next_rect):
            self.player_pos = next_pos

    def collect_pellets(self) -> None:
        player_center = (self.player_pos.x, self.player_pos.y)
        collect_distance = self.level.tile * 0.35

        remaining_pellets = []
        for pellet in self.level.pellets:
            pellet_x, pellet_y = self.level.grid_to_pixel_center(pellet)
            distance = pygame.Vector2(pellet_x, pellet_y).distance_to(player_center)
            if distance <= collect_distance:
                self.score += 10
            else:
                remaining_pellets.append(pellet)
        self.level.pellets = remaining_pellets

        remaining_power_pellets = []
        for pellet in self.level.power_pellets:
            pellet_x, pellet_y = self.level.grid_to_pixel_center(pellet)
            distance = pygame.Vector2(pellet_x, pellet_y).distance_to(player_center)
            if distance <= collect_distance:
                self.score += 50
            else:
                remaining_power_pellets.append(pellet)
        self.level.power_pellets = remaining_power_pellets

    def check_ghost_collision(self) -> bool:
        player_center = pygame.Vector2(self.player_pos.x, self.player_pos.y)
        min_distance = self.player_radius + self.ghost_radius - 4

        for ghost_pos in self.ghost_positions:
            if ghost_pos.distance_to(player_center) <= min_distance:
                return True
        return False

    def draw_ui(self) -> None:
        self.draw_text(f"Score: {self.score}", 10, 10)
        self.draw_text(f"Leben: {self.lives}", 10, 35)
        self.draw_text("Pfeile/WASD = Bewegung", 10, 60)
        self.draw_text("G = Grid | E = Entities | R = Neustart | K = Game Over", 10, 85)

        if not self.level.pellets and not self.level.power_pellets:
            win_surface = self.big_font.render("Alle Pellets eingesammelt!", True, (255, 255, 0))
            win_rect = win_surface.get_rect(center=(self.screen.get_width() // 2, 30))
            self.screen.blit(win_surface, win_rect)

    def update(self, dt: float) -> str | None:
        self.move_player(dt)
        self.collect_pellets()

        if self.check_ghost_collision():
            self.lives -= 1
            if self.lives <= 0:
                return "gameover"
            self._init_world_state()

        return None

    def draw(self) -> None:
        self.level.draw(self.screen)

        if self.show_grid:
            self.level.debug_draw_grid(self.screen)

        if self.show_entities:
            self.draw_entities()

        self.draw_ui()
        pygame.display.flip()

    def show_gameover(self) -> str:
        gameover = GameOverScreen(self.screen, title="Pac-Man")
        return gameover.run(score=self.score, message="Game Over")

    def run(self) -> str:
        self.running = True

        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                action = self.handle_event(event)

                if action == "quit":
                    return "quit"
                if action == "menu":
                    return "menu"
                if action == "restart":
                    self.reset()
                if action == "gameover":
                    gameover_action = self.show_gameover()
                    if gameover_action == "restart":
                        self.reset()
                    elif gameover_action == "menu":
                        return "menu"
                    else:
                        return "quit"

            update_action = self.update(dt)
            if update_action == "gameover":
                gameover_action = self.show_gameover()
                if gameover_action == "restart":
                    self.reset()
                elif gameover_action == "menu":
                    return "menu"
                else:
                    return "quit"

            self.draw()

        return "menu"