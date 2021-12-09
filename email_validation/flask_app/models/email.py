from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash 

class Email:
    db = 'email_validation_schema'
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO email_validation (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW())"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all_emails(cls):
        query = "SELECT * FROM email_validation"
        results = connectToMySQL(cls.db).query_db(query)
        add_emails = []
        for row in results:
            add_emails.append(cls(row))
        return add_emails 
    
    @staticmethod
    def is_valid(email):
        is_valid = True 
        query = "SELECT * FROM email_validation WHERE email = %(email)s"
        results = connectToMySQL(Email.db).query_db(query, email)
        if len(results) >= 1:
            flash("Email Taken")
            is_valid = False
        if not EMAIL_REGEX.match(email['email']):
            flash("Invalid Email")
            is_valid = False
        return is_valid 