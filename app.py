# Import required libraries
import os
from dotenv import load_dotenv
import requests
from typing import List

# Define constant variables for file paths and URLs
FILE_PATH: str = 'dane.txt'
GET_URL: str = 'https://poligon.aidevs.pl/dane.txt'
SEND_URL: str = 'https://poligon.aidevs.pl/verify'

# Load environment variables from .env file
load_dotenv()


def download_file(url: str, path: str) -> None:
    """Downloads a file from the given URL and saves it to the specified path"""
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)


def read_file(path: str) -> List[str]:
    """Reads a file line by line and returns a list of stripped lines"""
    lines = []
    with open(path, 'r') as file:
        for line in file.readlines():
            lines.append(line.strip())
    return lines


def get_data() -> List[str]:
    """Downloads data from URL, reads it, and removes the temporary file"""
    download_file(GET_URL, FILE_PATH)
    data = read_file(FILE_PATH)
    os.remove(FILE_PATH)  # Clean up temporary file
    return data


def send_data(data: dict) -> dict:
    """Sends POST request with JSON data and returns the response"""
    response = requests.post(SEND_URL, json=data)
    return response.json()


# Get data from the remote source
data: List[str] = get_data()

# Prepare the query dictionary with required fields
query: dict = {
    "task": os.getenv('TASK_NAME'),
    "apikey": os.getenv('AI_DEV_API_KEY'),
    "answer": data
}

# Send the data and print the response
response: dict = send_data(query)
print(response)
