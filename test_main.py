import unittest
import os
import csv
from main import process_characters, write_to_csv

# Configure test output for better error messages
unittest.TestCase.maxDiff = None  
unittest.TestCase.longMessage = True  

class TestRickAndMortyAPI(unittest.TestCase):
    
    def setUp(self):
        # Sample character data for testing
        self.sample_characters = [
            {
                "id": 1,
                "name": "Rick Sanchez",
                "status": "Alive",
                "species": "Human",
                "type": "",
                "gender": "Male",
                "origin": {
                    "name": "Earth (C-137)",
                    "url": "https://rickandmortyapi.com/api/location/1"
                },
                "location": {
                    "name": "Citadel of Ricks",
                    "url": "https://rickandmortyapi.com/api/location/3"
                },
                "image": "https://rickandmortyapi.com/api/character/avatar/1.jpeg",
                "episode": ["https://rickandmortyapi.com/api/episode/1"],
                "url": "https://rickandmortyapi.com/api/character/1",
                "created": "2017-11-04T18:48:46.250Z"
            }
        ]
        
        # Expected processed data
        self.expected_processed = [
            {
                "id": 1,
                "name": "Rick Sanchez",
                "status": "Alive",
                "species": "Human",
                "origin_name": "Earth (C-137)",
                "location_name": "Citadel of Ricks"
            }
        ]
        
        # Test CSV file name
        self.test_csv = "test_characters.csv"
    
    def tearDown(self):
        # Clean up test CSV file if it exists
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
    
    def test_process_characters(self):
        """Test that character processing extracts the correct fields"""
        processed = process_characters(self.sample_characters)
        self.assertEqual(processed, self.expected_processed, 
            "Character processing failed: Output does not match expected format")
    
    def test_write_to_csv(self):
        """Test that CSV writing works correctly"""
        write_to_csv(self.expected_processed, self.test_csv)
        
        # Verify the CSV file was created
        self.assertTrue(os.path.exists(self.test_csv), 
            f"CSV file '{self.test_csv}' was not created")
        
        # Read the CSV and verify contents
        with open(self.test_csv, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            self.assertEqual(len(rows), 1, 
                f"Expected 1 row in CSV, but found {len(rows)}")
            self.assertEqual(int(rows[0]["id"]), 1, 
                "Character ID mismatch in CSV")
            self.assertEqual(rows[0]["name"], "Rick Sanchez", 
                "Character name mismatch in CSV")
            self.assertEqual(rows[0]["status"], "Alive", 
                "Character status mismatch in CSV")
            self.assertEqual(rows[0]["species"], "Human", 
                "Character species mismatch in CSV")
            self.assertEqual(rows[0]["origin_name"], "Earth (C-137)", 
                "Character origin mismatch in CSV")
            self.assertEqual(rows[0]["location_name"], "Citadel of Ricks", 
                "Character location mismatch in CSV")


if __name__ == "__main__":
    unittest.main() 