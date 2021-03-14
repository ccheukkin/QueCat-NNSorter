import yaml
from pathlib import Path
import store.database
import categories.status

path = Path(__file__).parent / "./categories.yml"
with open(path) as file:
    yml = yaml.load(file, Loader=yaml.FullLoader)
    assert "categories" in yml.keys(), 'The key "categories" is not defined in the categories.yml file'
    categories = yml["categories"]
    categories = [] if categories == None else categories

    db = store.database.Database()
    catInDB = list(map(lambda x: x.name, db.categoryGetAll()))

    for c in categories:
        if not (c in catInDB):
            db.categoryCreate(c)

    for c in catInDB:
        if not(c in categories):
            if db.categoryInUse(c):
                confirm = input(f"{c} is in use by some records. Are you sure you want to delete it? Type 'y' to confirm\n")
                if confirm != "y":
                    continue
            db.categoryDelete(c)
