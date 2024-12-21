from sqlmodel import Session, create_engine, SQLModel

engine = create_engine('sqlite:///db.sqlite')

SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
