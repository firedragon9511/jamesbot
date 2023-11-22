import sqlite3, os

class DatabaseHandler:
    def __init__(self) -> None:
        self.custom_commands_db = 'db_custom_commands.db'
        self.guild_messages_db = 'db_guild_messages.db'


        if not os.path.exists(self.custom_commands_db):
            self.create_database_custom_commmand()
        
        if not os.path.exists(self.guild_messages_db):
            self.create_database_guild_messages()
        pass

    def create_database_custom_commmand(self):
        connection = sqlite3.connect(self.custom_commands_db)
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_data (
                Guild TEXT,
                Command TEXT,
                Result TEXT,
                PRIMARY KEY (Guild, Command)
            )
        ''')

        connection.commit()
        connection.close()

    def create_database_guild_messages(self):
        connection = sqlite3.connect(self.guild_messages_db)
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guild_messages (
                Guild TEXT,
                Channel TEXT,
                Welcome TEXT,
                Goodbye TEXT,
                PRIMARY KEY (Guild)
            )
        ''')

        connection.commit()
        connection.close()
        
        
    def update(self, db, query, params):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()


    def select_one(self, db, query, params):
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        connection.close()
        return result
    

    def update_guild_welcome(self, guild, channel = '', welcome = '', goodbye = ''):
        connection = sqlite3.connect(self.guild_messages_db)
        cursor = connection.cursor()
        cursor.execute(f'INSERT OR REPLACE INTO guild_messages (Guild, Channel, Welcome, Goodbye) VALUES ("{guild}", "{channel}", "{welcome}", "{goodbye}")')
        connection.commit()
        connection.close()
        #self.update(self.guild_messages_db, 'INSERT OR REPLACE INTO guild_messages (Guild, Welcome, Goodbye) VALUES (?, ?, ?)', (guild, welcome, goodbye))

    def insert_custom_command(self, guild, command, result):
        self.update(self.custom_commands_db, 'INSERT OR REPLACE INTO bot_data (Guild, Command, Result) VALUES (?, ?, ?)', (guild, command, result))


    def get_guild_messages(self, guild_id):
        return self.select_one(self.guild_messages_db, 'SELECT Channel, Welcome, Goodbye FROM guild_messages WHERE Guild = ?', (guild_id, ) )


    def get_custom_command(self, guild, command):
        connection = sqlite3.connect(self.custom_commands_db)
        cursor = connection.cursor()
        query = f'SELECT Result FROM bot_data WHERE Guild = \'{guild}\' AND Command = \'{command}\''
        print(query)
        cursor.execute(query)
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else None


if __name__ == "__main__":
    #DatabaseHandler().update_guild_message('test', '111111', 'Oláaa', 'Tchau')
    #print(DatabaseHandler().get_guild_messages('test'))

    '''if True:
        DatabaseHandler().create_database()'''
    pass