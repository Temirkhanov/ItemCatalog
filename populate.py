from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Category, Base, Item, User
from random import randint
engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

session.query(User).delete()
session.commit()

session.query(Category).delete()
session.commit()

session.query(Item).delete()
session.commit()

print("DELETED ALL ENTRIES!")
print("--------------------------")

try:
    User1 = User(name="Robo Barista",
                 email="tinnyTim@udacity.com", picture="hg")
    session.add(User1)
    session.commit()

    with open('data.txt', 'r+') as file:
        data = file.read().splitlines()

        i = 0
        while i < len(data):
            userID = randint(1, 3)
            cat = data[i]
            category = Category(user_id=userID, name=cat)
            session.add(category)
            session.commit()
            print(cat)
            while True:
                itemName = data[i+1]
                itemDescr = data[i+2]
                item = Item(name=itemName, description=itemDescr,
                            user_id=userID, category_id=category.id)
                #print(cat, itemName, itemDescr)
                print('- %s' % itemName)
                session.add(item)
                session.commit()
                if data[i+3] == '-':
                    i += 4
                    break
                i += 2
except:
    pass
finally:
    print("--------------------------")

print("--------------------------")
