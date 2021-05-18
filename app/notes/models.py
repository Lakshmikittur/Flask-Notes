from app import db

from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   


    def __init__(self,content, author_id):
        self.content = content
        self.author_id = author_id

    def serialize(self):
        return {
            'id': self.id,
            'date_created': f"{self.date_created}",
            'date_modified': f"{self.date_modified}",
            'content': self.content,
            'author_id': self.author_id
        }

    
