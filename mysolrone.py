import json
import pysolr
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define Solr connection
SOLR_URL = 'http://localhost:8983/solr/users'  # Update with your Solr URL and core name
solr = pysolr.Solr(SOLR_URL, timeout=10)

# Define the directory path containing JSON files
INPUT_DIR_PATH = '/home/user/Documents/demosolr/data/'  # Update with your input directory path

def load_json_file(file_path):
    """Load JSON data from a single file."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print(f"Data in file {file_path} is not a list.")
                return []
    except Exception as e:
        print(f"Failed to load JSON data from {file_path}: {e}")
        return []

def index_data_to_solr(data):
    """Index data into Solr."""
    if not data:
        print("No data to index.")
        return
    
    try:
        solr.add(data, commit=True)
        print(f"Indexed {len(data)} documents into Solr.")
    except Exception as e:
        print(f"Failed to index data into Solr: {e}")

def process_file(file_name):
    """Process a single file: load data and index to Solr."""
    file_path = os.path.join(INPUT_DIR_PATH, file_name)
    data = load_json_file(file_path)
    index_data_to_solr(data)

def main():
    """Main function to process files concurrently."""
    file_names = [f for f in os.listdir(INPUT_DIR_PATH) if f.endswith('.json')]
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks to the executor
        future_to_file = {executor.submit(process_file, file_name): file_name for file_name in file_names}
        
        # Wait for all tasks to complete
        for future in as_completed(future_to_file):
            file_name = future_to_file[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

if __name__ == "__main__":
    main()
