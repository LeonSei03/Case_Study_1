import os
from tinydb import TinyDB, Query
from serializer import serializer


class User:

    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')

    def __init__(self, id, name) -> None:
        """Create a new user based on the given name and id"""
        self.name = name #Anzeige-Name
        self.id = id #Email-Adresse

    def store_data(self)-> None:

        """Save the user to the database"""

        print("Storing user data")
        q = Query() #Query baut quasi einen Suchfilter
        
        existing = User.db_connector.search(q.id == self.id)
        
        if existing: 
            User.db_connector.update(self.__dict__, doc_ids=[existing[0].doc_id])
            print("User data updated")
        else: 
            User.db_connector.insert(self.__dict__)
            print("User data inserted")

    def delete(self) -> None:

        """Delete the user from the database"""

        q = Query ()

        existing = User.db_connector.search(q.id == self.id)

        if existing: 
            User.db_connector.remove(doc_ids=[existing[0].doc_id])
        
    
    def __str__(self):
        return f"User {self.id} - {self.name}"
    
    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def find_all(cls) -> list:
        """Find all users in the database"""

        users = []
        data = cls.db_connector.all()

        for u in data:
            user = cls(u["id"], u["name"])
            users.append(user)
        
        return users


    @classmethod
    def find_by_attribute(cls, by_attribute : str, attribute_value : str) -> 'User':
        """From the matches in the database, select the user with the given attribute value"""
        q = Query()
        result = cls.db_connector.search(q[by_attribute] == attribute_value)

        if result: 
            u = result[0]
            return cls(u["id"], u["name"])
        return None #wenn nichts gefunden 
