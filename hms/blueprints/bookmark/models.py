from hms.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class Bookmark(ResourceMixin, db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                                                  onupdate='CASCADE',
                                                  ondelete='CASCADE'),
                        index=True, nullable=False)
    
    name = db.Column(db.String(200), nullable=False)
    target = db.Column(db.String(2))
    parameter = db.Column(db.String(2000))
    
    def __init__(self, **kwargs):
        super(Bookmark, self).__init__(**kwargs)
