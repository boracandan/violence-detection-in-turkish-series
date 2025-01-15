from src.database.violence_detection_database import ViolenceDetectionDatabase
from src.download_and_transcription.add_clips_to_database import process_videos_in_parallel
from src.detection.detect_violence import analyse_transcripts_in_parallel
from src.download_and_transcription.transcribe import transcribe_audio_in_parallel
from os import environ

def main():
    # Initialize the connection with the database
    with ViolenceDetectionDatabase() as VDdb:
        # Load environment variables
        aaiApiKey = environ.get("AAI_API_KEY")
        openAiApiKey = environ.get("OPEN_AI_API_KEY")

        # Insert the links here
        links = ['https://www.youtube.com/watch?v=7H4jvc3ERrc', 'https://www.youtube.com/watch?v=Jg_x1fbZtsY',
                'https://www.youtube.com/watch?v=8aoHiS-HyFw', 'https://www.youtube.com/watch?v=JU9blLfDPuo',
                'https://www.youtube.com/watch?v=gsmyNL_-lD0', 'https://www.youtube.com/watch?v=oXT1SXqaWno',
                'https://www.youtube.com/watch?v=T2WB3DGJsz8', 'https://www.youtube.com/watch?v=1HgNReVRvzI',
                'https://www.youtube.com/watch?v=VVSDRN8Kh9s', 'https://www.youtube.com/watch?v=zXEY8j9Z0oI',
                'https://www.youtube.com/watch?v=aSozR1GKefY', 'https://www.youtube.com/watch?v=3TKbeZ3tNyY',
                'https://www.youtube.com/watch?v=g1Vag7OgCXw', 'https://www.youtube.com/watch?v=KtM2vZRvxnE',
                'https://www.youtube.com/watch?v=veM423POiU8', 'https://www.youtube.com/watch?v=f332DVN3EoQ',
                'https://www.youtube.com/watch?v=5WeGNZgmIxA', 'https://www.youtube.com/watch?v=NhVKrJ3uTt8',
                'https://www.youtube.com/watch?v=KHyLRPII8ow', 'https://www.youtube.com/watch?v=oTkv1jJ7fkQ',
                'https://www.youtube.com/watch?v=jCFH5UqMkfU']

        # Set the table name for the database 
        tableName = "SenAnlatKaradeniz"

        # Create table
        VDdb.create_table(tableName, 
                        episode_timeframe="TEXT NOT NULL PRIMARY KEY",
                        link="TEXT NOT NULL",
                        transcript="TEXT",
                        llm_violence_prediction="INT")

        # Add clips to the database and download them for transcription
        process_videos_in_parallel(tableName, links, VDdb)

        # Transcribe the clips
        transcribe_audio_in_parallel(aaiApiKey, tableName, VDdb)

        # Detect the percentage of violent clips (toward women)
        analyse_transcripts_in_parallel(openAiApiKey, tableName, VDdb)

        # Calculate Percentage
        data = VDdb.select_all(tableName, "llm_violence_prediction IS NOT ?", (None,))
        violentCount = 0
        for instance in data:
            if instance[3] == 1: # Check if the llm_violence_prediction is violent for the instance
                violentCount += 1
        violentPercentage = violentCount / len(data) * 100
        print(f"Violent Percentage: {violentPercentage}%")

if __name__ == "__main__":
    main()