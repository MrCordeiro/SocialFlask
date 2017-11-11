import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from peewee import *

DATABASE = SqliteDatabase('social.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    def get_posts(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):
        return Post.select().where(
            (Post.user << self.following()) | (Post.user == self)
            # << is equivalent to 'in' 
        )

    def following(self):
        """Returns the users we are following"""
        return (
            User.select().join(
                Relationship, on=Relationship.to_user #field being selected
            ).where(
                Relationship.from_user == self
            )
        )

    def followers(self):
        """Returns the users that are following us"""
        return (
            User.select().join(
                Relationship, on=Relationship.from_user
            ).where(
                Relationship.to_user == self
            )
        )

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin
                )
        except IntegrityError:
            raise ValueError("User already exixsts")


class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        rel_model=User, # model the foreign key points to
        related_name='posts' # if you were a User, how would you call the instances of this model?
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


class Relationship(Model):
    from_user = ForeignKeyField(
        rel_model=User, 
        related_name='relationships'
    )
    to_user = ForeignKeyField(
        rel_model=User,
        related_name='related_to'
    )

    class Meta:
        database = DATABASE
        indexes = (
            (('from_user', 'to_user'), True) # 'True' marks a unique index
        )

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Relationship], safe=True)
    DATABASE.close()