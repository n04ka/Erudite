class Scene:
    
    def __init__(self, f):
        self.f = f

    def draw(self):
        self.f()


class SceneSwitcher:

    window = None

    @staticmethod
    def clear():
        for widget in SceneSwitcher.window.winfo_children(): # type: ignore
            widget.destroy()

    @staticmethod
    def switch(scene):
        SceneSwitcher.clear()
        scene.draw()