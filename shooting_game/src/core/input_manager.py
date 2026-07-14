import pygame


class InputManager:
    def __init__(self) -> None:
        self.keys = pygame.key.get_pressed()
        self._fire_pressed = False
        self._fire_held = False
        self._fire_released = False
        self._bomb_pressed = False
        self._confirm_pressed = False
        self._up_pressed = False
        self._down_pressed = False
        self._charge_start = 0.0

    def poll(self) -> list[pygame.event.Event]:
        events = pygame.event.get()
        self.keys = pygame.key.get_pressed()

        self._fire_pressed = False
        self._fire_released = False
        self._bomb_pressed = False
        self._confirm_pressed = False
        self._up_pressed = False
        self._down_pressed = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_z, pygame.K_SPACE):
                    self._fire_pressed = True
                if event.key in (pygame.K_x,):
                    self._bomb_pressed = True
                if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                    self._confirm_pressed = True
                if event.key == pygame.K_UP:
                    self._up_pressed = True
                if event.key == pygame.K_DOWN:
                    self._down_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_z, pygame.K_SPACE):
                    self._fire_released = True

        self._fire_held = self.keys[pygame.K_z] or self.keys[pygame.K_SPACE]
        return events

    @property
    def left(self) -> bool:
        return self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]

    @property
    def right(self) -> bool:
        return self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]

    @property
    def up(self) -> bool:
        return self.keys[pygame.K_UP] or self.keys[pygame.K_w]

    @property
    def down(self) -> bool:
        return self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]

    @property
    def slow(self) -> bool:
        return self.keys[pygame.K_LSHIFT] or self.keys[pygame.K_RSHIFT]

    @property
    def fire_pressed(self) -> bool:
        return self._fire_pressed

    @property
    def fire_held(self) -> bool:
        return self._fire_held

    @property
    def fire_released(self) -> bool:
        return self._fire_released

    @property
    def bomb_pressed(self) -> bool:
        return self._bomb_pressed

    @property
    def confirm_pressed(self) -> bool:
        return self._confirm_pressed

    @property
    def up_pressed(self) -> bool:
        return self._up_pressed

    @property
    def down_pressed(self) -> bool:
        return self._down_pressed

    @property
    def pause_pressed(self) -> bool:
        return self.keys[pygame.K_ESCAPE] or self.keys[pygame.K_p]
