from PIL import Image
from customtkinter import CTkImage


class Settings:

    cfg: dict

    @staticmethod
    def load(verbose: bool = False):
        if verbose:
            print("Loading settings...", end="")
        Settings.cfg = dict()
        with open("settings.cfg", "r", encoding="utf-8") as f:
            for line in f:
                words = line.split()
                try:
                    value = int(words[1])
                except ValueError:
                    value = words[1]
                Settings.cfg.update({words[0] : value})
        if verbose:
            print("OK")


    @staticmethod
    def save(verbose: bool = True):
        if verbose:
            print("Saving settings...", end="")

        with open("settings.cfg", "w", encoding="utf-8") as f:
            for key, value in Settings.cfg.items():
                f.write(f"{key} {value}\n")

        if verbose:
            print("OK")
    

    @staticmethod
    def toggle_setting(key: str):
        Settings.cfg[key] = int(not Settings.cfg[key])
            


class Content:

    value: dict
    quantity: dict
    definition: dict
    textures: dict
    fonts: dict


    @staticmethod
    def load(verbose: bool = False):

        Content.value = dict()
        Content.quantity = dict()
        Content.definition = dict()
        Content.textures = dict()
        Content.fonts = dict()

        if verbose:
            print("Loading characters...", end="")

        with open("resources/characters.txt", "r", encoding="utf-8") as f:
            for line in f:
                words = line.split()
                Content.quantity.update({words[0] : int(words[1])})
                Content.value.update({words[0] : int(words[2])})

        if verbose:
            print("OK")
            print("Loading dictionary...", end="")

        with open("resources/words.txt", "r", encoding="utf-8") as f:
            for line in f:
                words = line.split(": ", 1)
                Content.definition.update({words[0] : words[1]})

        if verbose:
            print("OK")
            print("Loading textures...", end="")

        Content.textures.update({"ai-icon" : CTkImage(light_image=Image.open("resources/ai-icon.png"),
                                        dark_image=Image.open("resources/ai-icon.png"),
                                        size=(64, 64))})
        Content.textures.update({"human-icon" : CTkImage(light_image=Image.open("resources/human-icon.png"),
                                        dark_image=Image.open("resources/human-icon.png"),
                                        size=(64, 64))})
        if verbose:
            print("OK")
