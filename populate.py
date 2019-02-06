from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Category, Base, Item, User

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

print "DELETED ALL ENTRIES!"


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com", password="1234", picture="hg")
session.add(User1)
session.commit()

Category1 = Category(user_id=1, name="Category-1")
session.add(Category1)
session.commit()

Item1 = Item(user_id=1, name="Item 1.1", description="Blah blah blah", category=Category1) 
session.add(Item1)
session.commit()

Item2 = Item(user_id=1, name="Item 1.2", description="Blah blah blah", category=Category1) 
session.add(Item2)
session.commit()

Item3 = Item(user_id=1, name="Item 1.3", description="Blah blah blah", category=Category1) 
session.add(Item3)
session.commit()

Item4 = Item(user_id=1, name="Item 1.4", description="Blah blah blah", category=Category1) 
session.add(Item4)
session.commit()

# *************************************

Category2 = Category(user_id=1, name="Category-2")
session.add(Category2)
session.commit()

Item21 = Item(user_id=1, name="Item 2.1", description="Blah blah blah", category=Category2) 
session.add(Item21)
session.commit()

Item22 = Item(user_id=1, name="Item 2.2", description="Blah blah blah", category=Category2) 
session.add(Item22)
session.commit()

Item23 = Item(user_id=1, name="Item 2.3", description="Blah blah blah", category=Category2) 
session.add(Item23)
session.commit()

Item24 = Item(user_id=1, name="Item 2.4", description="Blah blah blah", category=Category2) 
session.add(Item24)
session.commit()

# ***************************************************

Category3 = Category(user_id=1, name="Category-3")
session.add(Category3)
session.commit()

Item31 = Item(user_id=1, name="Item 3.1", description="Blah blah blah", category=Category3) 
session.add(Item31)
session.commit()

Item32 = Item(user_id=1, name="Item 3.2", description="Blah blah blah", category=Category3) 
session.add(Item32)
session.commit()

Item33 = Item(user_id=1, name="Item 3.3", description="Blah blah blah", category=Category3) 
session.add(Item33)
session.commit()

Item34 = Item(user_id=1, name="Item 3.4", description="Blah blah blah", category=Category3) 
session.add(Item34)
session.commit()

# *******************************************

Category4 = Category(user_id=1, name="Category-4")
session.add(Category4)
session.commit()

Item41 = Item(user_id=1, name="Item 4.1", description="Blah blah blah", category=Category4) 
session.add(Item41)
session.commit()

Item42 = Item(user_id=1, name="Item 4.2", description="Blah blah blah", category=Category4) 
session.add(Item42)
session.commit()

Item43 = Item(user_id=1, name="Item 4.3", description="Blah blah blah", category=Category4) 
session.add(Item43)
session.commit()

Item44 = Item(user_id=1, name="Item 4.4", description="Blah blah blah", category=Category4) 
session.add(Item44)
session.commit()


print "***--=> CATEGORIES ADDED!"