from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, author):
        if not author:
            raise ValueError('Please provide an author name')
        
        existing_author = Author.query.filter(Author.name == author).first()
        #existing_author = db.session.query(Author.id).filter_by(name=author).first()

        if existing_author is not None:
            raise ValueError('Author name must be unique')
        
        return author
    
    @validates('phone_number')
    def validate_phone(self, key, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError('Please provide a proper 10-digit phone number')
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        list = ["Won't Believe", 'Secret', 'Top', 'Guess']
        for entry in list:
            if entry in title:
                return title
        raise ValueError('Title Wrong')
        

    @validates('content', 'summary')
    def validate_content(self, key, content):
        if key == 'content':
            if len(content) < 250:
                raise ValueError('Content wrong')
            return content
        if key == 'summary':
            if len(content) > 250:
                raise ValueError('Summary wrong')
            return content

    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Category wrong')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
