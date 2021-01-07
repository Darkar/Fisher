import json

class JsonData():
    def __init__(self):
        pass

    def ReadJson(self, file_path):
        try:
            with open(file_path, "r") as JsonFile:
                return json.load(JsonFile)
        except Exception as Error:
            return Error
        
    def WriteJson(self, file_path, data):
        try:
            json_data =  json.dumps(data, sort_keys=True, indent=4)
            with open(file_path, "a") as JsonFile:
                JsonFile.write(json_data)
        except Exception as Error:
            return Error