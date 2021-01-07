from bin.json_data import JsonData
import json 

class Config():
    def __init__(self):
        self.file_path = "config.json"
        self.config = JsonData().ReadJson(self.file_path)
    
    def __str__(self):
       return str(self.config)
    
    def App(self):
        return self.config["app"]

    def Settings(self):
        return self.config["settings"]