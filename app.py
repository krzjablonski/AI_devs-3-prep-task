# Import required libraries
import logging
from pathlib import Path
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define constant variables
FILE_PATH = Path('dane.txt')
GET_URL = 'https://poligon.aidevs.pl/dane.txt'
SEND_URL = 'https://poligon.aidevs.pl/verify'


def download_file(url: str, path: Path) -> None:
    """Downloads a file from the given URL and saves it to the specified path"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        path.write_bytes(response.content)
    except requests.RequestException as e:
        logger.error(f"Failed to download file: {e}")
        raise


def read_file(path: Path) -> List[str]:
    """Reads a file line by line and returns a list of stripped lines"""
    try:
        return [line.strip() for line in path.read_text().splitlines()]
    except IOError as e:
        logger.error(f"Failed to read file: {e}")
        raise


def get_data() -> List[str]:
    """Downloads data from URL, reads it, and removes the temporary file"""
    try:
        download_file(GET_URL, FILE_PATH)
        data = read_file(FILE_PATH)
        FILE_PATH.unlink(missing_ok=True)  # Clean up temporary file
        return data
    except Exception as e:
        logger.error(f"Failed to get data: {e}")
        raise


def send_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sends POST request with JSON data and returns the response"""
    try:
        response = requests.post(SEND_URL, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to send data: {e}")
        raise


def validate_config() -> None:
    """Validates that required environment variables are set"""
    required_vars = ['TASK_NAME', 'AI_DEV_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {missing_vars}")


def main() -> None:
    """Main function to orchestrate the data flow"""
    load_dotenv()
    validate_config()

    try:
        data = get_data()
        query = {
            "task": os.getenv('TASK_NAME'),
            "apikey": os.getenv('AI_DEV_API_KEY'),
            "answer": data
        }
        response = send_data(query)
        logger.info(f"Response received: {response}")
    except Exception as e:
        logger.error(f"Application failed: {e}")
        raise


if __name__ == '__main__':
    main()
