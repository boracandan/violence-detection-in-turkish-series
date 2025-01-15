import threading
import concurrent
import re

from src.database.violence_detection_database import ViolenceDetectionDatabase
from src.utils.functions import get_video_title, load_audio, return_search_ranges

def _add_to_database(VDdb: ViolenceDetectionDatabase, episodeNumber: str, range: tuple, videoLink: str, tableName: str, lock: threading.Lock) -> None:
    """
    Adds a new case to the database.

    Args:
        VDdb (ViolenceDetectionDatabase): The database object.
        episodeNumber (str): Episode number extracted from the video title.
        range (tuple): The time range for the clip (start, end).
        videoLink (str): Link to the video.
        tableName (str): Database table name to insert the case.
        lock (threading.Lock): Lock to ensure thread-safe database access.
    """
    case_identifier = f"{episodeNumber}:{range[0]}:{range[1]}"
    try:
        with lock:
            VDdb.add_case(tableName, case_identifier, videoLink)
            print(f"Added {case_identifier} to the database.")
    except Exception as e:
        print(f"Failed to add {case_identifier} to the database. Error: {e}")

def _process_video_link(videoLink: str, VDdb: ViolenceDetectionDatabase, tableName: str, lock: threading.Lock) -> None:
    """
    Processes a single video link to extract, download audio clips and add it to the database.

    Args:
        videoLink (str): The URL of the video to process.
        tableName (str): Database table name to associate the processed data.
    """
    searchRanges = return_search_ranges(videoLink)
    title = get_video_title(videoLink)
    episodeNumber = re.search(r"\d+", title).group()
    
    for range in searchRanges:
        load_audio(tableName, videoLink, "m4a", range)
        _add_to_database(VDdb, episodeNumber, range, videoLink, tableName, lock)


def process_videos_in_parallel(tableName: str, videoLinks: list[str], VDdb: ViolenceDetectionDatabase) -> None:
    """
    Processes multiple video links in parallel, extracting audio and updating the database.

    Args:
        tableName (str): Name of the database table to store processed data.
        videoLinks (list[str]): List of video URLs to process.
        VDdb (ViolenceDetectionDatabase): The database object to update.
    """
    lock = threading.Lock()
    # Loading all the peak audio clips concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for videoLink in videoLinks:
            executor.submit(_process_video_link, videoLink, VDdb, tableName, lock)