from app import db

class AccessCredential(db.Model):
    """Model for storing access credentials."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        """Convert the access credential to a dictionary."""
        return {
            'id': self.id,
            'service': self.service,
            'username': self.username,
            'password': self.password
        }
