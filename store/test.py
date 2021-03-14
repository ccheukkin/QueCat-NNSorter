import store.database

db = store.database.Database()

# db.createDB()
# db.categoryCreate("Bye")
# db.recordCreate("This is a question", ["Hello"])
# print(db.toCategoryId("Hello"))
print(db.categoryInUse("Hello"))