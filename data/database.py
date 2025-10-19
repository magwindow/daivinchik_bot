import aiosqlite

class Database:
    def __init__(self, name: str, table: str):
        self.name = name
        self.table = table
        
        
    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(20),
                age INTEGER(2),
                city VARCHAR(255),
                gender INTEGER(1),
                look_for INTEGER(1),
                about TEXT(500),
                photo VARCHAR(255)
                )"""
            await cursor.executescript(query)
            await db.commit()
            
    async def insert(self, **kwargs):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            await cursor.execute(
                """
                INSERT INTO users(
                    name, 
                    age, 
                    city, 
                    gender, 
                    look_for, 
                    about
                    ) VALUES (?, ?, ?, ?, ?, ?)""", **kwargs
                )
            await db.commit()