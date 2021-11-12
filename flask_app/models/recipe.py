from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Recipe:
    schema = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.name = data["name"]
        self.description = data["description"]
        self.under_30_mins = data["under_30_mins"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = user.User.get_by_id({"id": data["user_id"]})


    @classmethod
    def create(cls, data):
        query = """INSERT INTO recipes (name, description, under_30_mins, instructions, date_made, created_at, updated_at, user_id)
                VALUES (%(name)s, %(description)s, %(under_30_mins)s, %(instructions)s, %(date_made)s, NOW(), NOW(), %(user_id)s);"""

        return connectToMySQL(cls.schema).query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.schema).query_db(query)

        recipes = []
        for row in results:
            recipes.append(cls(row))

        return recipes


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)

        if len(results) < 1:
            return False

        return cls(results[0])


    @classmethod
    def update(cls, data):
        query = """UPDATE recipes SET name = %(name)s, description = %(description)s, under_30_mins = %(under_30_mins)s, 
                instructions = %(instructions)s, date_made = %(date_made)s, updated_at = NOW()
                WHERE id = %(id)s;"""

        return connectToMySQL(cls.schema).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        connectToMySQL(cls.schema).query_db(query, data)


    @staticmethod
    def validate(post_data):
        print(post_data)
        is_valid = True

        if len(post_data["name"]) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False

        if len(post_data["description"]) < 4:
            flash("Description must be at least 4 characters.")
            is_valid = False

        if len(post_data["instructions"]) < 4:
            flash("Instructions must be at least 4 characters.")
            is_valid = False

        return is_valid
