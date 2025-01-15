from src.database import ViolenceDetectionDatabase
from src.download_and_transcription.add_clips_to_database import process_videos_in_parallel
from src.detection.detect_violence import analyse_transcripts_in_parallel
from src.download_and_transcription.transcribe import transcribe_audio_in_parallel
from os import environ

if __name__ == "__main__":
    # Initialize the connection with the database
    with ViolenceDetectionDatabase() as VDdb:
        # Load environment variables
        aaiApiKey = environ.get("AAI_API_KEY")
        openAiApiKey = environ.get("OPEN_AI_API_KEY")

        # The links of the first 20 episodes from Yalı Çapkını
        links = ['https://www.youtube.com/watch?v=-u_RlLqmopg', 'https://www.youtube.com/watch?v=DehYOOQiLgI', 'https://www.youtube.com/watch?v=60CyQKY3_GU', 'https://www.youtube.com/watch?v=JgY_nQAagfA', 'https://www.youtube.com/watch?v=1Qtj1sc5ZD8', 'https://www.youtube.com/watch?v=NHp77VkKde8', 'https://www.youtube.com/watch?v=NS4f-BumfeQ', 'https://www.youtube.com/watch?v=Fyvo9ED9ne0', 'https://www.youtube.com/watch?v=kzJyjEl4HP8', 'https://www.youtube.com/watch?v=m9xQgFhoxhQ', 'https://www.youtube.com/watch?v=b2ug1fPzTO0', 'https://www.youtube.com/watch?v=Vm73DHrzeOY', 'https://www.youtube.com/watch?v=D1x11DqhkgU', 'https://www.youtube.com/watch?v=MHHEFaPq17Y', 'https://www.youtube.com/watch?v=Znku4orP2j4', 'https://www.youtube.com/watch?v=pp5jAdtiMTk', 'https://www.youtube.com/watch?v=PKmeEezCRgg', 'https://www.youtube.com/watch?v=QocqrBOYwlY', 'https://www.youtube.com/watch?v=JVjA62ax9Bo', 'https://www.youtube.com/watch?v=UcXraVnJRl8']

        # Set the table name for the database 
        tableName = "YalıÇapkını"

        # Create table
        VDdb.create_table(tableName, 
                        episode_timeframe="TEXT NOT NULL PRIMARY KEY",
                        link="TEXT NOT NULL",
                        transcript="TEXT",
                        violence="INT",
                        llm_violence_prediction="INT")

        # Add clips to the database and download them for transcription
        process_videos_in_parallel(tableName, links, VDdb)

        # Transcribe the clips
        transcribe_audio_in_parallel(aaiApiKey, tableName, VDdb)

        # Get the LLM's answers for whether the transcripts are violent/non-violent towards women
        analyse_transcripts_in_parallel(openAiApiKey, tableName, VDdb)