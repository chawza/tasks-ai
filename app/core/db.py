from sqlmodel import Session, SQLModel, create_engine

engine = create_engine('sqlite:///db.sqlite')

SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
