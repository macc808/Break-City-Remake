import sys


class Scene:
    def __init__(self, name):
        self.name = name

    def start(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass


class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def register_scene(self, scene):
        self.scenes[scene.name] = scene

    def set_scene(self, name):
        if name not in self.scenes:
            raise ValueError(f"Scene '{name}' is not registered")

        self.current_scene = self.scenes[name]
        if hasattr(self.current_scene, "start"):
            self.current_scene.start()

    def handle_event(self, event):
        if self.current_scene is not None:
            self.current_scene.handle_event(event)

    def update(self, dt):
        if self.current_scene is not None:
            self.current_scene.update(dt)

    def draw(self, screen):
        if self.current_scene is not None:
            self.current_scene.draw(screen)


