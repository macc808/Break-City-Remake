import pygame


class Engine:
    """Core physics and collision utilities."""

    def __init__(self):
        self.ignored_objects = set()

    def update(self, *args, **kwargs):
        # Placeholder for future physics updates (gravity, velocity, friction)
        return None

    def collide_sprite_group(self, sprite, group, dokill=False, collided=None):
        """Collide a single sprite against a group."""
        return pygame.sprite.spritecollide(sprite, group, dokill, collided)

    def collide_groups(self, groupa, groupb, dokill_a=False, dokill_b=False, collided=None):
        """Collide two groups."""
        return pygame.sprite.groupcollide(groupa, groupb, dokill_a, dokill_b, collided)


