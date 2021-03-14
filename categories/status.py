import yaml
from pathlib import Path
from colorama import init
import store.database


init()
ADD = '\033[32m'
NORMAL = '\033[90m'
REMOVE = '\033[31m'
END = '\033[0m'


path = Path(__file__).parent / "./categories.yml"
with open(path) as file:
    yml = yaml.load(file, Loader=yaml.FullLoader)
    assert "categories" in yml.keys(), 'The key "categories" is not defined in the categories.yml file'
    categories = yml["categories"]

    db = store.database.Database()
    catInDB = list(map(lambda x: x.name, db.categoryGetAll()))

    print("The following categories will be added to or are already in the database:")
    for c in categories:
        addTag = NORMAL+" " if c in catInDB else ADD+"+"
        print(f"{addTag} {c}{END}")
    
    print("The following categories will be deleted from the database:")
    for c in catInDB:
        if not(c in categories):
            inUseTag = "*" if db.categoryInUse(c) else " "
            print(f"{inUseTag} {REMOVE}{c}{END}")
    print("Note that the * means that the category is in use by some record in the database")
        


