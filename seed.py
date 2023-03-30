from app import app
from models import db, User, Feedback

db.drop_all()
db.create_all()

u1 = User.register(username='Catman', password="goodpassword", email='myemail@mail.com', first_name="Danny", last_name='Bagels')
u2 = User.register(username='Unstoppable', password="beans2Night", email='mailofmine@cool.com', first_name="Danantha", last_name='Joeson')
u3 = User.register(username='Smellyguy2', password="Beeseatfree", email='mailofme@cool.com', first_name="Gretch", last_name='Boiler')
u4 = User.register(username='Goodguy4you', password="Beeseatfree2night", email='mailthatismine@cool.com', first_name="French", last_name='Stench')

db.session.add_all([u1,u2,u3,u4])
db.session.commit()

f1 = Feedback(title='Cool Beans', content="I really liked it in short all i can say is cool beans", username='Catman')
f2 = Feedback(title='Cool Beans 2', content="I really liked a second time too! again in short all i can say is cool beans", username='Catman')
f3 = Feedback(title='uncool', content="I really didn't like it ngl, kinda rough, next time better", username='Unstoppable')
f4 = Feedback(title='uncool to the max', content="I would have to agree with unstoppable, next time better for sure... no bueno!", username='Smellyguy2')

db.session.add_all([f1,f2,f3,f4])
db.session.commit()
