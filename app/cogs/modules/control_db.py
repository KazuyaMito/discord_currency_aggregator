from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.dialects.mysql import BIGINT as Bigint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, orm, ForeignKey
from urllib.parse import urlparse
import os

Base = declarative_base()
url = urlparse(os.environ['DATABASE_URL'])
engine = create_engine("mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8".format(url.username, url.password, url.hostname, url.path[1:]))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Bigint(unsigned=True), nullable=False, unique=True)
    user_name = Column(String(255), nullable=False)
    use_count = Column(INTEGER(unsigned=True), nullable=False, server_default="0")


class Guild(Base):
    __tablename__ = "guilds"
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    is_name_read = Column(Boolean, nullable=False, server_default="False")
    is_multi_line_read = Column(Boolean, nullable=False, server_default="False")
    dictionary = orm.relationship("Dictionary")


class Dictionary(Base):
    __tablename__ = "dictionaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(255))
    read = Column(String(255))
    guild_id = Column(String(255), ForeignKey('guilds.id', onupdate='CASCADE', ondelete='CASCADE'))


def main():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()


Session = orm.sessionmaker(engine)
session = Session()


def add_user(user_id, user_name, use_count):
    user = User(user_id=user_id, user_name=user_name, use_count=use_count)

    session.add(user)
    session.commit()


def get_user(user_id):
    return session.query(User).filter_by(user_id=user_id).one_or_none()


def get_users():
    return session.query(User).all()


def update_user_use_count(user, use_count):
    user.use_count = use_count
    session.commit()


def delete_all_users():
    session.query(User).delete()
    session.commit()


def get_guild(guild_id):
    return session.query(Guild).filter_by(id=guild_id).one_or_none()


def add_guild(guild_id, name):
    guild = Guild(id=guild_id, name=name)

    session.add(guild)
    session.commit()


def add_dictionary(word, read, guild_id):
    dictionary = session.query(Dictionary).filter_by(word=word, guild_id=guild_id).one_or_none()
    print(dictionary)
    if isinstance(dictionary, type(None)):
        dictionary = Dictionary(word=word, read=read, guild_id=guild_id)

        session.add(dictionary)
        session.commit()
    else:
        set_dictionary(read, dictionary)


def set_dictionary(read, dictionary):
    dictionary.read = read
    session.commit()


def get_dictionary(word, guild_id):
    return session.query(Dictionary).filter_by(word=word, guild_id=guild_id).one_or_none()


def get_dictionaries(guild_id):
    return session.query(Dictionary).filter_by(guild_id=guild_id)


def delete_dictionary(id, guild_id):
    dictionary = session.query(Dictionary).filter_by(id=id, guild_id=guild_id).one_or_none()

    if isinstance(dictionary, type(None)):
        return None
    else:
        session.delete(dictionary)
        session.commit()
        return True


def set_read_name(read_name, guild_id):
    guild = get_guild(guild_id=guild_id)

    guild.is_name_read = read_name
    session.commit()


def set_read_multi_line(read_multi, guild_id):
    guild = get_guild(guild_id=guild_id)

    guild.is_multi_line_read = read_multi
    session.commit()