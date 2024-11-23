from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert


def get_or_create(session: Session, model, defaults=None, **kwargs):
    defaults = defaults or {}
    instance = session.query(model).filter_by(**kwargs).one_or_none()

    if instance:
        return instance, False
    else:
        # Merge defaults with kwargs for creating a new instance
        params = {**kwargs, **defaults}
        instance = model(**params)

        try:
            session.add(instance)
            session.commit()
            return instance, True
        except IntegrityError:
            session.rollback()
            instance = session.query(model).filter_by(**kwargs).one()
            return instance, False
