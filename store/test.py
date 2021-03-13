import database

db = database.Database()

# db.createDB()
# db.categoryCreate("Hello")
db.recordCreate("This is a question", ["Hello"])
# print(db.toCategoryId("Hello"))