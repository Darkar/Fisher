import configparser

class Config():
    def __init__(self, filepath = "fisher.conf"):
        self.filepath = filepath
        self.config = configparser.ConfigParser()

    def __getitem__(self, item):
        try:
            self.config.read(self.filepath)
            return self.config[item]
        except KeyError:
            print("Fichier de configuration introuvable !")
            exit(0)
