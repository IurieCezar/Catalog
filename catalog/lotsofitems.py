#!/usr/bin/python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit().

session = DBSession()

# Create dummy user
User1 = User(name='John Doe',
             email='jdoe@mail.com',
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png'
             )
session.add(User1)
session.commit()


# Create sport categories
category1 = Category(name='Soccer', user_id=1)

session.add(category1)
session.commit()

# Create sport items
Item1 = Item(
    user_id=1,
    title='Balls',
    description='Training Soccer Balls',
    category=category1,
    image='grasshopper.jpg'
    )

session.add(Item1)
session.commit()

Item2 = Item(
    user_id=1,
    title='Nets',
    description='Instant Soccer Goal',
    category=category1,
    image='grasshopper.jpg'
    )

session.add(Item2)
session.commit()

Item3 = Item(
    user_id=1,
    title='Soccer Score Books & Clipboards',
    description='Franklin Soccer Coaching Clipboards',
    category=category1,
    image='grasshopper.jpg'
    )

session.add(Item3)
session.commit()

Item4 = Item(
    user_id=1,
    title='Cleats',
    description='The best on the market!',
    category=category1,
    image='grasshopper.jpg'
    )

session.add(Item4)
session.commit()

Item5 = Item(
    user_id=1,
    title='Socks',
    description='Reebok All Sport Athletic Knee High Socks',
    category=category1,
    image='grasshopper.jpg'
    )

session.add(Item5)
session.commit()

Item6 = Item(
    user_id=1,
    title='Shorts',
    description='Umbro Youth Rio Check Shorts',
    category=category1,
    image='grasshopper.jpg'
    )

session.add(Item6)
session.commit()

Item7 = Item(
    user_id=1,
    title='Shirts and Tops',
    description='Adidas Estro 15 Short Sleeve Soccer Jersey',
    category=category1,
    image='grasshopper.jpg'
    )

session.add(Item7)
session.commit()

Item8 = Item(
    user_id=1,
    title='Goalkeeper Apparel & Protection',
    description='adidas Entry Goalkeeping Jersey',
    category=category1,
    image='grasshopper.jpg'
    )

session.add(Item8)
session.commit()

Item9 = Item(
    user_id=1,
    title='Head Guard',
    description='Storelli ExoShield Head Guard',
    category=category1,
    image='grasshopper.jpg'
    )

session.add(Item9)
session.commit()


category2 = Category(user_id=1, name='Basketball')

session.add(category2)
session.commit()

Item1 = Item(
    user_id=1,
    title='Basketballs',
    description='Wilson NCAA All-Surface Rubber Official Basketball',
    category=category2,
    image='grasshopper.jpg'
    )

session.add(Item1)
session.commit()

Item2 = Item(
    user_id=1,
    title='Hoops',
    description='Goaliath In-Ground Basketball Hoop with Pole Pad',
    category=category2,
    image='grasshopper.jpg'
    )

session.add(Item2)
session.commit()

Item3 = Item(
    user_id=1,
    title='Training Equipment',
    description='Ballback Pro Basketball Ball Return System',
    category=category2,
    image='grasshopper.jpg'
    )

session.add(Item3)
session.commit()

Item4 = Item(
    user_id=1,
    title='Court Equipment',
    description='Pole & Backboard Pads',
    category=category2,
    image='grasshopper.jpg'
    )

session.add(Item4)
session.commit()

Item5 = Item(
    user_id=1,
    title='Arm & Leg Sleeves',
    description='McDavid HEX Extended Leg Sleeves - Pair',
    category=category2,
    image='grasshopper.jpg'
    )

session.add(Item5)
session.commit()

Item6 = Item(
    user_id=1,
    title='Apparel & Socks',
    description='Nike Elite Long Sleeve Basketball Shirt',
    category=category2,
    image='grasshopper.jpg'
    )

session.add(Item6)
session.commit()


category3 = Category(user_id=1, name='Baseball')

session.add(category3)
session.commit()

Item1 = Item(
    user_id=1,
    title='Footwear',
    description='Under Armour Leadoff RM Baseball Cleats',
    category=category3,
    image='grasshopper.jpg'
    )

session.add(Item1)
session.commit()

Item2 = Item(
    user_id=1,
    title='Bats',
    description='Easton Mako Youth Bat 2016',
    category=category3,
    image='grasshopper.jpg'
    )

session.add(Item2)
session.commit()

Item3 = Item(
    user_id=1,
    title='Gloves & Mitts',
    description='Rawlings T-Ball Player Series Glove wBall',
    category=category3,
    image='grasshopper.jpg'
    )

session.add(Item3)
session.commit()

Item4 = Item(
    user_id=1,
    title='Apparel & Uniforms',
    description='Lightweight, durable and comfortable',
    category=category3,
    image='grasshopper.jpg'
    )

session.add(Item4)
session.commit()

Item5 = Item(
    user_id=1,
    title='Batting Gloves',
    description='Under Armour Youth Clean-Up VI Batting Gloves',
    category=category3,
    image='grasshopper.jpg'
    )

session.add(Item5)
session.commit()


category4 = Category(user_id=1, name='Frisbee')

session.add(category4)
session.commit()

Item1 = Item(
    user_id=1,
    title='Discs',
    description='Discraft 175 gram Ultra Star Sport Disc',
    category=category4,
    image='grasshopper.jpg'
    )

session.add(Item1)
session.commit()

Item2 = Item(
    user_id=1,
    title='Clets',
    description='The Best Ultimate Frisbee Cleats',
    category=category4,
    image='grasshopper.jpg'
    )

session.add(Item2)
session.commit()

Item3 = Item(
    user_id=1,
    title='Cones',
    description='Orange, all shapes',
    category=category4,
    image='grasshopper.jpg'
    )

session.add(Item3)
session.commit()

Item4 = Item(
    user_id=1,
    title='Gloves',
    description='All colors',
    category=category4,
    image='grasshopper.jpg'
    )

session.add(Item4)
session.commit()

Item5 = Item(
    user_id=1,
    title='Backpacks',
    description='Big and small',
    category=category4,
    image='grasshopper.jpg'
    )

session.add(Item5)
session.commit()

Item6 = Item(
    user_id=1,
    title='Other equipment',
    description='From adidas',
    category=category4,
    image='grasshopper.jpg'
    )

session.add(Item6)
session.commit()


category5 = Category(user_id=1, name="Snowboarding")

session.add(category5)
session.commit()

Item1 = Item(
    user_id=1,
    title='Snowboards',
    description='Burton Youth Riglet 2014-2015 Snowboard',
    category=category5,
    image='grasshopper.jpg'
    )

session.add(Item1)
session.commit()

Item2 = Item(
    user_id=1,
    title='Boots',
    description='Head Shine 2017 DieCut',
    category=category5,
    image='grasshopper.jpg'
    )

session.add(Item2)
session.commit()

Item3 = Item(
    user_id=1,
    title='Bindings',
    description='Head NX Fay One Snowboard Bindings',
    category=category5,
    image='grasshopper.jpg'
    )

session.add(Item3)
session.commit()

Item4 = Item(
    user_id=1,
    title='Protective Gear',
    description='Triple Eight Undercover Snowboarding Wrist Guards',
    category=category5,
    image='grasshopper.jpg'
    )

session.add(Item4)
session.commit()

Item5 = Item(
    user_id=1,
    title='Helmets',
    description='Giro Adult Bevel Snow Helmet',
    category=category5,
    image='grasshopper.jpg'
    )

session.add(Item5)
session.commit()


category6 = Category(user_id=1, name="Rock Climbing")

session.add(category6)
session.commit()

Item1 = Item(
    user_id=1,
    title='Boots',
    description='La Sportiva Nepal EVO GTX Mountaineering Boots',
    category=category6,
    image='grasshopper.jpg'
    )

session.add(Item1)
session.commit()

Item2 = Item(
    user_id=1,
    title='Petzl',
    description='Petzl GRIGRI 2 Belay Device',
    category=category6,
    image='grasshopper.jpg'
    )

session.add(Item2)
session.commit()

Item3 = Item(
    user_id=1,
    title='Cams',
    description='Black Diamond Camalot C4 Cams',
    category=category6,
    image='grasshopper.jpg'
    )

session.add(Item3)
session.commit()

Item4 = Item(
    user_id=1,
    title='Tents',
    description='The North Face VE-25 Tents',
    category=category6,
    image='grasshopper.jpg'
    )

session.add(Item4)
session.commit()

Item5 = Item(
    user_id=1,
    title='Ropes',
    description='Mammut Infinity 9.5mm x 70m Duodess Single Dry Ropes',
    category=category6,
    image='grasshopper.jpg'
    )

session.add(Item5)
session.commit()


category7 = Category(user_id=1, name='Foosbal')

session.add(category7)
session.commit()

Item1 = Item(
    user_id=1,
    title='Tables',
    description='Best tables ever made',
    category=category7,
    image='grasshopper.jpg'
    )

session.add(Item1)
session.commit()

Item2 = Item(
    user_id=1,
    title='Bumper',
    description='Rubberized',
    category=category7,
    image='grasshopper.jpg'
    )

session.add(Item2)
session.commit()

Item3 = Item(
    user_id=1,
    title='Bearings',
    description='Durable',
    category=category7,
    image='grasshopper.jpg'
    )

session.add(Item3)
session.commit()

Item4 = Item(
    user_id=1,
    title='Guards',
    description='Rubberized',
    category=category7,
    image='grasshopper.jpg'
    )

session.add(Item4)
session.commit()

Item5 = Item(
    user_id=1,
    title='Rods',
    description='Best ever',
    category=category7,
    image='grasshopper.jpg'
    )

session.add(Item5)
session.commit()

Item6 = Item(
    user_id=1,
    title='Levelers',
    description='Waerior Levelers(feet)',
    category=category7,
    image='grasshopper.jpg'
    )

session.add(Item6)
session.commit()

Item7 = Item(
    user_id=1,
    title='Handles',
    description='Warrior handles',
    category=category7,
    image='grasshopper.jpg'
    )

session.add(Item7)
session.commit()


category8 = Category(user_id=1, name='Skating')

session.add(category8)
session.commit()

Item1 = Item(
    user_id=1,
    title='Skates',
    description='Ice skates such as Jackson Mystique',
    category=category8,
    image='grasshopper.jpg'
    )

session.add(Item1)
session.commit()

Item2 = Item(
    user_id=1,
    title='Gloves',
    description='For men and women',
    category=category8,
    image='grasshopper.jpg'
    )

session.add(Item2)
session.commit()


category9 = Category(user_id=1, name='Hockey')

session.add(category9)
session.commit()

Item1 = Item(
    user_id=1,
    title='Hockey skates',
    description='Mission Inhaler DSG:5 Senior Roller Hockey Goalie Skates',
    category=category9,
    image='grasshopper.jpg'
    )

session.add(Item1)
session.commit

Item2 = Item(
    user_id=1,
    title='Helmets',
    description='Reebok 11K Hockey Helmet',
    category=category9,
    image='grasshopper.jpg'
    )

session.add(Item2)
session.commit()

Item3 = Item(
    user_id=1,
    title='Sticks',
    description='Warrior Dynasty HD1 Clear Intermediate Hockey Stick',
    category=category9,
    image='grasshopper.jpg'
    )

session.add(Item3)
session.commit()

print 'added category items!'
