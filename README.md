
# A Transcription-Based Violence Detection Program (Towards Women) in Turkish TV Series

## A fully functional violence (towards women) detection project written in Python using AssemblyAI for transcription and OpenAI's GPT-4o for analysis processes

This README is available in both English and Turkish:

- [English Version](README.md)
- [Türkçe Versiyon](README.tr.md)

This project was built as part of the TÜBİTAK 2204-A research project, which comprehensively addresses the impact of violence towards women on Turkish society and culture. The project is entirely written in Python, and the process follows these steps:

1. **Data Scraping from YouTube**: The seconds of the peak viewership/engagement points of the TV series were determined by scraping data from YouTube.
2. **Audio Clip Extraction**: From these points, the top 15% with the highest repeated views were selected, and 90-second audio clips (45 seconds before and after the peak) were extracted from those segments.
3. **Transcription Using AssemblyAI**: The downloaded audio clips were transcribed using AssemblyAI’s speaker diarization method, which is a leading AI in the modern speech processing industry, known for providing more accurate results in performance tests than any other models (See: [AssemblyAI Benchmark](https://assemblyaiassets.com/pdf/2024%20Speech%20AI%20Benchmarks.pdf)).
4. **Analysis with OpenAI GPT-4o**: The resulting transcripts were then provided to OpenAI's GPT-4o model, which is known for its advanced reasoning and understanding capabilities (See: [OpenAI GPT-4o Documentation](https://platform.openai.com/docs/models/gpt-4o)). The model was tasked with identifying whether any form of violence against women (psychological, physical, economic, etc.) was present in the given transcripts, based on custom prompts.
5. **Violence Analysis**: Finally, the percentage of violence towards women in the most popular scenes of the series was calculated by analyzing the results, identifying the ratio of violent content in the most viewed sections of the episodes.

## Project Structure

All the logic behind the program is contained in the `src` package, and an example usage demonstration is provided in the `main.py` file. Additionally, the `accuracy_testing` directory demonstrates how we tested the accuracy percentage of OpenAI's GPT-4o for our specific task.

## Requirements

The project requires the following dependencies to be installed:

- `AssemblyAI` for transcription
- `OpenAI` for GPT-4o analysis
- `yt-dlp` for downloading YouTube videos
- `ffmpeg` for audio processing
- Other dependencies listed in the `requirements.txt` file

### Note: 
- **FFmpeg** needs to be installed manually by the user. You can download FFmpeg from [FFmpeg Official Site](https://ffmpeg.org/download.html) and follow the installation instructions for your platform.

You can install the necessary packages using:

pip install -r requirements.txt

## Configuration

The project uses `pyproject.toml` to manage build system and packaging configurations. Make sure to check this file if you're looking to customize project settings, package the project, or manage dependencies.

## Usage

To use this project, follow the instructions in `main.py` for demonstrating the process. Make sure you have your API keys for AssemblyAI and OpenAI set up in a `.env` file (an example is given with the '.env.example' file).

---

Feel free to open an issue or contribute to this project to enhance its functionality further.
