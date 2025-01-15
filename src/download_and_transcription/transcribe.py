import concurrent.futures
import threading
import assemblyai as aai
from os import listdir

import concurrent
from src.database.violence_detection_database import ViolenceDetectionDatabase
import re

def _update_database(VDdb: ViolenceDetectionDatabase, tableName: str, PATH: str, transcript: str, lock: threading.Lock) -> None:
  """
    Updates the database with the transcript for a given audio file.

    Args:
        VDdb (ViolenceDetectionDatabase): The database object to update.
        tableName (str): Name of the database table to update.
        PATH (str): Path to the audio file.
        transcript (aai.Transcript): Transcription object containing transcript data.
        lock (threading.Lock): Lock to ensure thread-safe database access.
    """
  with lock:
    try:
      digitsInPath = re.findall(r"\d+", PATH)
      episodeNumber, startTime = digitsInPath[0], ":".join(digitsInPath[1:4])
      transcriptText = " | ".join([f"Speaker {utterance.speaker}: {utterance.text}" for utterance in transcript.utterances])
      VDdb.update_case(tableName, f"{episodeNumber}:{startTime}", transcript=transcriptText)
    except Exception as e:
      print(f"Error updating database for {PATH}: {e}")

def _transcribe_audio(PATH: str, VDdb: ViolenceDetectionDatabase, tableName: str, transcriber: aai.Transcriber, config: aai.TranscriptionConfig, lock: threading.Lock) -> None:
  """
    Transcribes an audio file and updates the database with the transcript.

    Args:
        PATH (str): Path to the audio file to transcribe.
        VDdb (ViolenceDetectionDatabase): The database object to update.
        tableName (str): Name of the database table to update.
        transcriber (aai.Transcriber): AssemblyAI transcriber object.
        config (aai.TranscriptionConfig): Configuration object for transcription.
        lock (threading.Lock): Lock to ensure thread-safe database access.
  """
  try:
    transcript = transcriber.transcribe(PATH, config=config)
    _update_database(VDdb, tableName, PATH, transcript, lock)
    print(f"Successfully added {PATH}'s transcript to the database.")
  except Exception as e:
        print(f"Error transcribing audio {PATH}: {e}")

def transcribe_audio_in_parallel(apiKey: str, tableName: str, VDdb: ViolenceDetectionDatabase) -> None:
  """
    Transcribes multiple audio files in parallel and updates the database.

    Args:
        apiKey (str): API key for AssemblyAI.
        tableName (str): Name of the database table to update.
        VDdb (ViolenceDetectionDatabase): The database object to update.
    """
  # Replace with your API key
  aai.settings.api_key = apiKey

  # PATHS of the file to transcribe
  FILE_PATHS = [f"audios/{tableName}Audios/{file}" for file in listdir(f"audios/{tableName}Audios")]

  config = aai.TranscriptionConfig(speaker_labels=True, language_code="tr")

  transcriber = aai.Transcriber()
  
  lock = threading.Lock()

  with concurrent.futures.ThreadPoolExecutor() as executor:
    for PATH in FILE_PATHS:
      executor.submit(_transcribe_audio, PATH, VDdb, tableName, transcriber, config, lock)



