from sqlalchemy import or_

from hms.extensions import db
from lib.util_sqlalchemy import ResourceMixin

#tags = db.Table('tags',
#                db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
#                db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
#                )


class Post(ResourceMixin, db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)

    # Relationships.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=False)
#    tags = db.relationship('Tag', secondary=tags,
#                           backref=db.backref('posts', lazy='dynamic'))

    title = db.Column(db.String(280), nullable=False)
    body = db.Column(db.String(2000))
    coded_body = db.Column(db.String(4000))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Post, self).__init__(**kwargs)

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (Post.title.ilike(search_query),
                        Post.body.ilike(search_query))

        return or_(*search_chain)


class Tag(ResourceMixin, db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)

    # Relationships.
#    post_id = db.Column(db.Integer, db.ForeignKey('posts.id',
#                                                  onupdate='CASCADE',
#                                                  ondelete='CASCADE'),
#                        index=True, nullable=False)

    name = db.Column(db.String(40))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Tag, self).__init__(**kwargs)


class Comment(ResourceMixin, db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)

    # Relationshops.
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=False)

    body = db.Column(db.String(1000))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(Comment, self).__init__(**kwargs)
