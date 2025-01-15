import os
import sqlite3 as sq

class ViolenceDetectionDatabase():
    """
    A database class specifically created for the detection of violence toward women in TV series 
    via the extraction and analysis of transcripts.
    """
    def __init__(self, dbPath: str = "./data/violeneDetection.db") -> None:
        self.conn = sq.connect(dbPath, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # try:   
        #     self.cursor.execute\
        #     ("""CREATE TABLE YalıÇapkını (
        #         episode_timeframe TEXT NOT NULL PRIMARY KEY,
        #         link TEXT NOT NULL,
        #         transcript TEXT,
        #         violence INT,
        #         llm_violence_prediction INT 
        #     ); """)
        # except:
        #     pass 

        # try:   
        #     self.cursor.execute\
        #     ("""CREATE TABLE Hercai (
        #         episode_timeframe TEXT NOT NULL PRIMARY KEY,
        #         link TEXT NOT NULL,
        #         transcript TEXT,
        #         llm_violence_prediction INT 
        #     ); """)
        # except:
        #     pass 
        
    def __enter__(self) -> "ViolenceDetectionDatabase":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.conn.close()

    def db_console(self) -> None:
        """A function to interact with the database via the console."""
        query = input("Query: ")
        self.cursor.execute(query)
        resultList = self.cursor.fetchall()
        self.conn.commit()
        print(resultList)

    def create_table(self, tableName: str, **kwargs) -> None:
        """
        A function to create a table with the specified table name and columns in the database.
        
        Args:
            tableName (str): The name of the table to be created.
            **kwargs: Column names of the table and their SQL types (e.g., `columnName='TEXT NOT NULL'`).

        """
        # Create the audio directory for the table if it doesn't exist
        audio_directory = os.path.join("audios", f"{tableName}Audios")
        os.makedirs(audio_directory, exist_ok=True)  # Creates the directory if it doesn't exist

        # SQL code to create a table
        columns = ", ".join([f"{item[0]} {item[1]}" for item in kwargs.items()])
        query = f"""CREATE TABLE IF NOT EXISTS {tableName} ({columns});"""
        self.cursor.execute(query)
    
    def add_case(self, tableName: str, episodeAndTimeframe: str, link: str, **kwargs) -> None:
        """
        A method to add an element to the specified table of the database.

        Args:
            tableName (str): The name of the table of the case to be added.
            episodeAndTimeframe (str): The episode and timeframe information of the instance to be added (e.g., '1:00:58:45:00:59:50').
            link (str): The link information of the instance to be added.
            **kwargs: Columns to be added and their values (e.g., `columnName=value`).
        
        """
        # Extract the query's elements
        columnsToInsert = "(" + ", ".join(["episode_timeframe", "link"] + [key for key in kwargs.keys()]) + ")"
        values = (episodeAndTimeframe, link) + tuple(kwargs.values())
        placeHolders = "(" + ", ".join(["?" for _ in range(2 + len(kwargs))]) + ")"
        
        self.cursor.execute(f"""INSERT INTO {tableName} {columnsToInsert} VALUES {placeHolders}""", values)
        self.conn.commit()
    
    def update_case(self, tableName: str, episodeAndTimeframe: str, **kwargs) -> None:
        """
        A method to update an element from the stated table's columns to the values given.
        
        Args:
            tableName (str): The name of the table of the case to be updated.
            episodeAndTimeframe (str): The episode and timeframe information of the instance to be updated (e.g., '1:00:58:45:00:59:50'). 
            **kwargs: Columns to be updated and their new values (e.g., `columnName=value`).

        """
        valuesToUpdate = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        
        self.cursor.execute(f"""UPDATE {tableName} SET {valuesToUpdate} WHERE episode_timeframe LIKE (?)""", list(kwargs.values()) + [f"{episodeAndTimeframe}%"])
        self.conn.commit()
    
    def select_all(self, tableName: str, whereClause: str = None, params: tuple = ()) -> list:
        """
        A function to select all the elements that align with the where clause (if given) from the specified table of the database, and return them in a list.
        
        Args:
            tableName (str): The name of the table of the items to be selected.
            whereClause (str): The columns that you want to put the constraints on (e.g., whereClause='columnName=?').
            params (tuple): The values of constraints in order.

        """
        if whereClause:
            query = f"SELECT * FROM {tableName} WHERE {whereClause} ORDER BY episode_timeframe ASC"
            self.cursor.execute(query, params)
        
        else:
            self.cursor.execute(f"SELECT * FROM {tableName} ORDER BY episode_timeframe ASC")
        
        resultList = self.cursor.fetchall()
        return resultList



# with ViolenceDetectionDatabase() as VDdb:
#     r = VDdb.select_all("SenAnlatKaradeniz", "llm_violence_prediction IS  ?", (None,))
#     print(len(r))
    # violentCount = 0
    # for instance in r:
    #     if instance[4] == 1:
    #         violentCount += 1
    # violentPercentage = violentCount / len(r) * 100
    # print(f"Violent Percentage: {violentPercentage}%")

#     FILE_PATHS = [f"audios/HercaiAudios/{file}" for file in listdir("audios/HercaiAudios")]
#     print(len(FILE_PATHS))
    
    # VDdb.update_case("12:02:06:44", transcript= "Speaker A: Hepsi benim suçum dede bu masadaki kimse söylediklerini hak etmiyor. Bak bana! (Tokat atar.)")
    # VDdb.cursor.execute("PRAGMA table_info(Hercai);")

    # print(VDdb.cursor.fetchall())

    # data = VDdb.select_all("Sen")
    # print(data, len(data))
    # VDdb.update_case('9:01:51:39:01:53:09', llm_violence_prediction=None)
    # VDdb.cursor.execute("SELECT * FROM YalıÇapkını WHERE llm_violence_prediction IS NOT ? AND violence IS NOT ?", (None, None))
    # resultList = VDdb.select_all("Sen", "llm_violence_prediction IS ?", (None,))
    # print(resultList, len(resultList))
    # VDdb.update_case("1:00:34:10", transcript=None)
    # VDdb.cursor.execute("UPDATE YalıÇapkını SET llm_violence_prediction2 = NULL")
    # VDdb.cursor.execute("DROP TABLE Sen")
    # VDdb.conn.commit()
    # resultList = VDdb.cursor.fetchall()
    # print(resultList)
    # VDdb.cursor.execute("DELETE FROM SenAnlatKaradeniz WHERE llm_violence_prediction IS NULL")
    # VDdb.conn.commit()

    