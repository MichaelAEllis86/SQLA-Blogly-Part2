from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)

#models go below


class User(db.Model):
    """Users model. A user could have many posts"""

    __tablename__ = "users"

    def __repr__(self):
        u=self
        return f"<user id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url} "

    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    first_name=db.Column(db.String(50),
                        nullable=False,
                        unique=False)
    last_name=db.Column(db.String(50),
                        nullable=False,
                        unique=False)
    image_url=db.Column(db.Text, 
                        nullable=True,
                        unique=False,
                        default='https://i.imgur.com/SHxfpjI.jpg'
                        )
    
    post_info=db.relationship("Post", cascade="all, delete-orphan")
    
    # posts=db.relationship("Posts", backref="Users")
#problem exists with image_url model will not accept strings longer than 50, creates a pyscopig error -------->Fixed by changing db.column type to text and recreating db!
#problem exits with default image, for one it doens't work because of imgur's anti-display code in a img tag, also the default is not filling when the form is left blank ----->Need to fix!

class Post(db.Model):
    """Posts model, a post has one user/creator"""

    
    def format_date(self):

        months={1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        month_key=self.created_at.month
        named_month=months[month_key]
        friendly_time=self.created_at.strptime(f'{self.created_at.hour}:{self.created_at.minute}','%H:%M').strftime('%I:%M %p')
        
        return f"{named_month} {self.created_at.day}, {self.created_at.year} at {friendly_time}"

    @classmethod
    def print_current_time(self):
        print(f"{datetime.now()}")
        return(f"{datetime.now()}")
    
    __tablename__ = "posts"

    def __repr__(self):
        p=self
        return f"<post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id} "
    
    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    title=db.Column(db.String(50),
                        nullable=False,
                        unique=False)
    content=db.Column(db.Text, 
                        nullable=False,
                        unique=False,
                        )
    created_at=db.Column(db.DateTime,
                         nullable=False,
                         default=datetime.now())
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))

    user_info=db.relationship("User")
    
    
    
    

    
    