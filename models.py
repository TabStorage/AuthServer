from app import db, bcrypt

class User(db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(100), nullable=False)

    def __init__(self, email, password, username):
        self.email = email
        self.set_password(password)
        self.username = username

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def validated_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return self.username