# -*- coding: utf-8 -*-

from app import db
from app.models import User, File

def show_users():
    for user in User.query.all():
        print(user)

def show_files():
    for saved_file in File.query.all():
        print(saved_file)

def show_user_by_name(name, *args):
    if name:
        for user in User.query.filter_by(username=name).all():
            print(user)
    if args:
        for arg in args:
            for user in User.query.filter_by(username=arg).all():
                print(user)

def show_file_by_name(name, *args):
    if name:
        for saved_file in File.query.filter_by(source_filename=name).all():
            print(saved_file)
    if args:
        for arg in args:
            for saved_file in File.query.filter_by(source_filename=arg).all():
                print(saved_file)

def delete_users():
    for user in User.query.all():
        db.session.delete(user)
        db.session.commit()

def delete_files():
    for saved_file in File.query.all():
        db.session.delete(saved_file)
        db.session.commit()

def delete_user_by_name(name, *args):
    if name:
        for user in User.query.filter_by(username=name).all():
            db.session.delete(user)
    if args:
        for arg in args:
            for user in User.query.filter_by(username=arg).all():
                db.session.delete(user)
    db.session.commit()

def delete_file_by_name(name, *args):
    if name:
        for saved_file in File.query.filter_by(source_filename=name).all():
            db.session.delete(saved_file)
    if args:
        for arg in args:
            for saved_file in File.query.filter_by(source_filename=arg).all():
                db.session.delete(saved_file)
    db.session.commit()

if __name__ == "__main__":
    delete_users()
    delete_files()