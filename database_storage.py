import serializer
from tinydb import TinyDB

class Database:
    def __init__(self, db_path):
        self.db = TinyDB(db_path)

    def setup_db(self):
        # Create table if it doesn't exist
        self.db.table('temperature_data')

    def store_data(self, data,topic_name):
       #store data
       print(f"Storing data in topic {topic_name}: {data}")
       self.db.table(topic_name)
       self.db.table(topic_name).insert(data)
       

    def get_recent_temperatures(self, limit):
        # Retrieve the recent temperature entries sorted by insertion time
        recent_entries = self.db.table('temperature_data').all()
        recent_entries.sort(key=lambda x: x.doc_id, reverse=True)  # Sort by insertion order (doc_id)
        recent_entries = recent_entries[:limit]
        return recent_entries