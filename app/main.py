#!/usr/bin/env python3
import requests
import csv
import logging
import sys
from typing import Dict, List, Any

# Set up simplified logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('rick_and_morty_api')

# API Constants
API_BASE_URL = "https://rickandmortyapi.com/api"
CHARACTER_ENDPOINT = f"{API_BASE_URL}/character"
CSV_OUTPUT_FILE = "characters.csv"
CSV_FIELD_NAMES = ["id", "name", "status", "species", "origin_name", "location_name"]


def fetch_characters(url: str = CHARACTER_ENDPOINT) -> List[Dict[str, Any]]:
    """
    Fetch characters from the Rick and Morty API, handling pagination.
    
    Args:
        url: The API URL to fetch data from
        
    Returns:
        A list of character dictionaries
    """
    all_characters = []
    page = 1
    
    try:
        while url:
            logger.info(f"Fetching page {page}...")
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            all_characters.extend(data["results"])
            
            # Check if there's a next page
            url = data.get("info", {}).get("next")
            page += 1
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: {e}")
        raise
    
    logger.info(f"Fetched {len(all_characters)} characters successfully")
    return all_characters


def process_characters(characters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process character data to extract required fields.
    
    Args:
        characters: List of character dictionaries from the API
        
    Returns:
        List of processed character dictionaries with selected fields
    """
    processed_characters = []
    
    for character in characters:
        processed_character = {
            "id": character["id"],
            "name": character["name"],
            "status": character["status"],
            "species": character["species"],
            "origin_name": character["origin"]["name"],
            "location_name": character["location"]["name"]
        }
        processed_characters.append(processed_character)
    
    return processed_characters


def write_to_csv(characters: List[Dict[str, Any]], filename: str = CSV_OUTPUT_FILE) -> None:
    """
    Write character data to a CSV file.
    
    Args:
        characters: List of processed character dictionaries
        filename: Output CSV filename
    """
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELD_NAMES)
            writer.writeheader()
            writer.writerows(characters)
        
        logger.info(f"Created {filename} with {len(characters)} character records")
    
    except IOError as e:
        logger.error(f"Error writing file: {e}")
        raise


def main():
    """Main function to orchestrate the data extraction and processing."""
    try:
        # Fetch all characters from the API
        characters = fetch_characters()
        
        # Process character data
        processed_characters = process_characters(characters)
        
        # Write to CSV
        write_to_csv(processed_characters)
        
        logger.info("Process completed successfully")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 