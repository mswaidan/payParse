from app import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64), index=True, unique=False)
    type = db.Column(db.String(64), index=True, unique=False)
    
    def __repr__(self):
        return '<Date %r>' % (self.date)


