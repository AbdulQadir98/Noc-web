import os

class NocturneFramework:
    def __init__(self, greeting="Hello"):
        self.greeting = greeting

    def say_hello(self, name):
        return f"{self.greeting}, {name}!"

    def get_models(self):
        folder_path = "app/models"
        extension = ".pt"

        # Get the list of models with pt extension
        files = [file for file in os.listdir(
            folder_path) if file.endswith(extension)]

        return files
