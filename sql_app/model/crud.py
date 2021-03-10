from sqlalchemy.orm import Session
from sql_app.schemas.User import UserCreate
from sql_app.schemas.Ressource import RessourceCreate
from sql_app.schemas.Consulter import FavoriteCreate
from sql_app.model import models
from datetime import datetime
from sql_app.custom.RessourceType import RessourceTypeEnum
from sql_app.custom.CategoryLabel import CategoryEnum


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id_user == user_id).one()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.mail_user == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).all()


def create_user(db: Session, user: UserCreate):
    db_user = models.User()
    db_user.firstname = user.firstname
    db_user.lastname = user.lastname
    db_user.mail_user = user.mail
    db_user.zip_code_user = user.zip_code
    db_user.pseudo_user = user.pseudo
    db_user.password_user = user.password + "secret"
    db_user.birthdate_user = user.birthdate
    db_user.created_at_user = datetime.today()
    if user.role == 'citoyen connecté':
        db_user.id_roles = 2
    elif user.role == 'admin':
        db_user.id_roles = 3
    elif user.role == 'super admin':
        db_user.id_roles = 4
    elif user.role == 'modérateur':
        db_user.id_roles = 5
    else:
        db_user.id_roles = 1
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_ressources(db: Session):
    return db.query(models.Ressource).all()


def get_ressource(db: Session, ressource_id: int):
    return db.query(models.Ressource).filter(models.Ressource.id_res == ressource_id).one()


def get_ressource_by_type(db: Session, ressource_type: RessourceTypeEnum):
    return db.query(models.Ressource).filter(models.Ressource.id_type_res == ressource_type).all()


def get_ressource_by_category_label(db: Session, label_cat: CategoryEnum):
    return db.query(models.Ressource).join(models.Caracterise).filter(models.Caracterise.id_cat == label_cat).all()


def get_relation_res(db: Session, relation: str):
    return db.query(models.Relation).filter(models.Relation.label_rel == relation).one()


def get_category_res(db: Session, category: str):
    return db.query(models.Category).filter(models.Category.label_cat == category).one()


def create_ressource(db: Session, ressource: RessourceCreate):
    db_ressource = models.Ressource()
    db_ressource.title_res = ressource.title_res
    db_ressource.status_res = 'Pending'
    db_ressource.acces_res = ressource.acces_res
    db_ressource.content_res = ressource.content_res
    db_ressource.source_res = ressource.source_res
    db_ressource.created_at_res = datetime.today()
    db_ressource.difficulty = ressource.difficulty
    db_ressource.id_user = ressource.user

    if ressource.type_ressource == 'jeu':
        db_ressource.id_type_res = 1
    elif ressource.type_ressource == 'atelier':
        db_ressource.id_type_res = 3
    else:
        db_ressource.id_type_res = 2

    db.add(db_ressource)
    db.flush()

    relation = get_relation_res(db, ressource.relation_res)
    db_valable = models.EstValable()
    db_valable.id_rel = relation.id_rel
    db_valable.id_res = db_ressource.id_res
    db.add(db_valable)
    db.flush()

    category = get_category_res(db, ressource.category_res)
    db_caracterise = models.Caracterise()
    db_caracterise.id_cat = category.id_cat
    db_caracterise.id_res = db_ressource.id_res
    db.add(db_caracterise)
    db.flush()

    db.commit()
    db.refresh(db_ressource)
    return db_ressource


def create_favorite(db: Session, favorite: FavoriteCreate):
    db_fav = models.Consulter()
    db_fav.id_res = favorite.id_res
    db_fav.id_user = favorite.id_user
    db_fav.favorite = favorite.favorite
    db_fav.start_date = datetime.today()
    if favorite.note_user is not None:
        db_fav.note_user = favorite.note_user
    else:
        db_fav.note_user = 0

    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav
