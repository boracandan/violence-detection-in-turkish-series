import subprocess
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
import re
import requests as req

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

def timeToComplete(func: callable) -> callable:
    """
    Decorator to measure and return the time taken by a function to execute.
    """
    def inner(*args, **kwargs):
        startTime = time.time()
        returnValue = func(*args, **kwargs)
        endTime = time.time()
        return (returnValue, endTime - startTime)
    return inner

def convert(time: int | str) -> int | str:
    """
    Converts time between seconds (int) and HH:MM:SS (str) formats.
    
    Args:
        time (int or str): Time in seconds (int) or HH:MM:SS format (str).
    
    Returns:
        int or str: Converted time in the other format.
    """
    if isinstance(time, int):
        hours = time // 3600
        minutes = (time - hours*3600) // 60
        seconds = time - hours*3600 - minutes*60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    elif isinstance(time, str):
        totalSeconds = 0
        hoursMinutesSeconds = list(map(int, time.split(":")))
        for index, timeElement in enumerate(hoursMinutesSeconds[::-1]): # Reversing the list to get elements in the order: sec, min, hour
             totalSeconds += 60 ** index * timeElement
        return totalSeconds
    
def return_search_ranges(videoLink: str) -> list[tuple[str]]:
    """
    Extracts heatmap data from a YouTube video and calculates search ranges around peak points.
    
    Args:
        videoLink (str): The URL of the YouTube video.
    
    Returns:
        list[tuple[str]]: A list of time ranges (start, end) where peaks were detected in the heatmap.
    """
    options = webdriver.ChromeOptions()
    # Instructs Chrome to run in the background without any GUI
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Opens Video Link
    driver.get(videoLink)
    
    # Wait for the heat-map-path to render
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    heatMapData = soup.find("path", class_="ytp-heat-map-path").get("d")
    videoDuration = convert(soup.find("span", class_="ytp-time-duration").text) # format = hr:min:sec

    # Close the browser
    driver.quit()

    # Extracting the x and y-values from the raw heat map data using regex
    findings = re.findall(r"[MCL](?: -?\d+[.]\d+,-?\d+[.]\d+){2} (\d+[.]\d+),(\d+[.]\d+)", heatMapData)
    
    xValues = [(float(finding[0]) - 5)/1000 for finding in findings]     # We substract 5 to get rid of the offset
    yValues = [(100-float(finding[1]))/100 for finding in findings]

    peaks = find_peak_points(yValues, xValues, 15/100)
    ranges = find_search_ranges(peaks, 90, videoDuration)

    return ranges

def find_peak_points(yValues: list, xValues: list, percent: float) -> list[tuple]:
    """
    Finds peak points in the heatmap data.

    Args:
        yValues (list): Normalized y-values from the heatmap.
        xValues (list): Normalized x-values from the heatmap.
        percent (float): Percentage of top peaks to retain (e.g., 0.15 for 15%).

    Returns:
        list[tuple]: List of (time, value) tuples for the top peaks.
    """
    peakElements = []
    yValues = [float("-inf")] + yValues + [float("-inf")]
    for i in range(1, len(yValues) - 1):
        if yValues[i-1] < yValues[i] > yValues[i+1]:
            peakElements.append((xValues[i - 1], yValues[i]))
    
    # Only take the top x percent of points based upon their y-value
    numOfElementsToTake = round(percent * len(peakElements))
    return sorted(peakElements, key=lambda peakElement: peakElement[1])[-numOfElementsToTake:]

def find_search_ranges(peakPoints: list, searchLength: int, duration: int) -> list[tuple]:
    """
    Converts peak points into search time ranges.

    Args:
        peakPoints (list[tuple]): List of (time, value) tuples for the peaks.
        searchLength (int): Length of the search window in seconds.
        duration (int): Total video duration in seconds.

    Returns:
        list[tuple]: List of (start_time, end_time) time ranges.
    """
    searchRanges = []
    for peakPoint in peakPoints:
        peakTime = peakPoint[0] * duration
        startTime, endTime = peakTime - searchLength // 2, peakTime + searchLength // 2
        if startTime >= 0 and endTime <= duration: # Check if the search range is valid
            searchRanges.append((convert(int(startTime)), convert(int(endTime))))
    return searchRanges

def get_video_title(link: str) -> str:
    """
    Returns the title of the video specified

    Args:
        link (str): The link of the video that you want to get the title of.

    Returns:
        str: The title of the video.
    """
    html = req.get(link)
    soup = BeautifulSoup(html.content, "lxml")
    title = soup.find("title").text
    return title

def load_audio(tableName: str, link: str, fileType: str, sectionToDownload: tuple[str]) -> None:
    """
    Downloads the audio segment of the specified time intervals in the stated file type of the video given.

    Args:
        tableName (str): The name of the database table (used to give the download directory it's name).
        link (str): The Youtube video URL.
        fileType (str): The desired audio file format (e.g., 'm4a').
        sectionToDownload (tuple): A tuple containing the start and end times of the time interval to be downloaded in a 'HH:MM:SS' format.
    """
    start, end = sectionToDownload[0], sectionToDownload[1]
    # command = f'yt-dlp -f "bestvideo[ext={fileType}][height<={resolutionHeight}]+bestaudio[ext={fileType}]/best[ext={fileType}][height<={resolutionHeight}]" -P videos --external-downloader ffmpeg \
    #             --external-downloader-args "ffmpeg_i: -ss {start} -to {end}" "{link}"'
    command = f'yt-dlp -f "bestaudio[ext={fileType}]" -P audios/{tableName}Audios -o "%(title)s{start}.%(ext)s" --external-downloader ffmpeg \
            --external-downloader-args "ffmpeg_i: -ss {start} -to {end}" "{link}"'

    p1 = subprocess.run(command, shell=True, capture_output=True)
    
    if p1.returncode != 0:
        print(f"Error downloading audio: {p1.stderr.decode()}")
    else:
        print(f"Audio downloaded successfully for range {start} to {end}.")




