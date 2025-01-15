import concurrent.futures
import json
import openai
from src.database.violence_detection_database import ViolenceDetectionDatabase

from tenacity import (
  retry,
  stop_after_attempt,
  wait_random_exponential,
)  # for exponential backoff

import concurrent
import threading


@retry(wait=wait_random_exponential(min=1, max=75), stop=stop_after_attempt(10))
def _run_conversation(client: openai.OpenAI, content: str) -> dict:
    """
    Sends a transcript to the OpenAI API for classification.

    Args:
        client (openai.OpenAI): The OpenAI API client.
        content (str): The transcript content to be classified.

    Returns:
        dict: The API response containing the classification result.
    """
    # Define the system message to properly instruct the assistant 
    systemMessage = "Türk dizilerinden alınmış transkriptleri kadına yönelik şiddet içeren (1) veya şiddet içermeyen (0) olarak sınıflandıran bir asistansın. Şiddet fiziksel, \
                psikolojik, vb. türlerden olabilir. Belirsizliğe mahal vermeyen ve net noktalarda şiddet var diyeceksin."
    
    messages = [{"role": "user", "content": content}, 
               {"role": "system", "content": systemMessage}]
    
    tools = [{
        "type": "function",
        "function": {
            "name": "insert_violence_data",
            "description": "Kadına yönelik şiddet içeren (1) ya da içermeyen (0) olarak aldığı \
            yanıtları database'e göderir.",
            "parameters": {
            "type": "object",
            "properties": {
                "classification": {
                    "type": "integer",
                    "description": "Transkriptin şiddet içerme durumu (1 ya da 0)"
                }
            },
            "required": ["classification"]
        }
      }
    }]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice= {"type": "function", "function": {"name": "insert_violence_data"}},
        temperature=0.4  # Lower temperature for more deterministic behavior  
    )

    return response


def _update_database(llmAnswer: str, VDdb: ViolenceDetectionDatabase, tableName: str, episodeAndTimeframe: str, lock: threading.Lock) -> None:
    """
    Updates the database with the classification result.

    Args:
        llmAnswer (str): The classification result from the assistant.
        VDdb (ViolenceDetectionDatabase): The database instance.
        tableName (str): The name of the database table.
        episodeAndTimeframe (str): The unique identifier for the episode and timeframe.
        lock (threading.Lock): A threading lock to ensure thread safety.
    """
    with lock:
        VDdb.update_case(tableName, episodeAndTimeframe, llm_violence_prediction=int(llmAnswer))


def _process_transcript(transcript: str, VDdb: ViolenceDetectionDatabase, tableName: str, episodeAndTimeframe: str, lock: threading.Lock, client: openai.OpenAI) -> None:
    """
    Processes a single transcript by sending it to the OpenAI API and updating the database.

    Args:
        transcript (str): The transcript content.
        VDdb (ViolenceDetectionDatabase): The database instance.
        tableName (str): The name of the database table.
        episodeAndTimeframe (str): The unique identifier for the episode and timeframe.
        lock (threading.Lock): A threading lock to ensure thread safety.
        client (openai.OpenAI): The OpenAI API client.
    """
    try:
        response = _run_conversation(client, transcript)
        print(response)
        
        # Extract the return value from function call
        function = response.choices[0].message.tool_calls[0].function
        arguments = json.loads(function.arguments)
        
        llmAnswer = arguments.get("classification", None)
        

        if llmAnswer is not None:
            # Update the database 
            _update_database(llmAnswer, VDdb, tableName, episodeAndTimeframe, lock)
            print(f"Updated the database for the instance {episodeAndTimeframe}.")

    except Exception as e:
        print(f"Error processing transcript for {episodeAndTimeframe}: {str(e)}")


def analyse_transcripts_in_parallel(apiKey: str, tableName: str, VDdb: ViolenceDetectionDatabase) -> None:
    """
    Analyzes transcripts in parallel by classifying them and updating the database.

    Args:
        apiKey (str): The API key for the OpenAI service.
        tableName (str): The name of the database table.
        VDdb (ViolenceDetectionDatabase): The database instance.
    """
    # Initializing OpenAI API
    client = openai.OpenAI(api_key=apiKey)

    # Defining the threading lock
    lock = threading.Lock()

    # Getting the data from the database
    data = VDdb.select_all(tableName, "llm_violence_prediction IS ?", (None,))

    with concurrent.futures.ThreadPoolExecutor() as executer:
        for instance in data:
            executer.submit(_process_transcript, instance[2], VDdb, tableName, instance[0], lock, client)
    


