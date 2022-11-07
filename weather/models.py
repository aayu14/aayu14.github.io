from weather import db


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


    def __init__(self,name):
        self.name=name
    


#Creating  Database Tables

db.create_all()
