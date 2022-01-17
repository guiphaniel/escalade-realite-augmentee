from src.model.database import Database
from src.view.manager import Manager


def processMenu():
    disp = Manager(1920,1080)
    disp.start()

processMenu()

database = Database()
database.insert("string", "value")

