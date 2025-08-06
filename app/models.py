# DB 모델 정의

from app import db

class Club(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    description = db.Column(db.String(45))
    tags = db.Column(db.String(45))
    sns_link = db.Column(db.String(225))
    application_period = db.Column(db.String(45))
    application_form = db.Column(db.String(225))
    booth_location = db.Column(db.String(100))

    def __repr__(self):
        return f"<Club {self.id} - {self.name}>"
