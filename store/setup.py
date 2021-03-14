import store.database
from pathlib import Path
import store.database

asked = []
def ask(question, default):
    defaultVal = f"[{default}]" if default else ""
    user = input(f"{question}{defaultVal}: ")
    user = default if not user else user
    asked.append(f"{question}: {user}")
    return user

print("Enter information for connecting to MySql database. [] means default value.")
username = ask("Database username", None)
password = ask("Database password", None)
database = ask("Database name", "nnsorter")
ip = ask("Database IP", "localhost")
port = ask("Port number", "3306")

print("\nWhat you have enterd:")
for a in asked:
    print(a)

path = Path(__file__).parent / "./.env"
with open(path, "w") as f:
    f.write(f"DATABASE_URL='mysql+mysqldb://{username}:{password}@{ip}:{port}/{database}'")

db = store.database.Database()
db.createDB()