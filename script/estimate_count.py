import mysql.connector
from mysql.connector import Error
import csv
import datetime
import os
import pathlib
import configparser
import shutil

# Get the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the counts directory (parent of script directory)
COUNTS_DIR = os.path.dirname(SCRIPT_DIR)

def read_config():
    """Read configuration from properties file"""
    config = configparser.ConfigParser()
    config_path = os.path.join(COUNTS_DIR, 'properties', 'config.properties')
    config.read(config_path)
    return config

# Read configuration
config = read_config()

# Define input and output directories from config
INPUT_DIR = config['Directories']['count_output_dir']
OUTPUT_DIR = config['Directories']['estimate_output_dir']

def clean_estimate_directory():
    """Delete all files in the estimate directory"""
    if os.path.exists(OUTPUT_DIR):
        for filename in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Error deleting {file_path}: {e}')
        print(f"Cleaned directory: {OUTPUT_DIR}")
    else:
        print(f"Directory does not exist: {OUTPUT_DIR}")

def read_sql_file(filepath):
    with open(filepath, 'r') as file:
        return file.read().strip()

def split_queries(sql_content):
    # Split on semicolon but ignore semicolons within comments
    queries = []
    current_query = []
    in_comment = False
    
    for line in sql_content.split('\n'):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Handle comments
        if line.startswith('/*'):
            in_comment = True
            continue
        if line.startswith('*/'):
            in_comment = False
            continue
        if line.startswith('--') or in_comment:
            continue
            
        # Handle USE statements
        if line.upper().startswith('USE '):
            continue
            
        # Add non-comment lines to current query
        if ';' in line:
            current_query.append(line)
            queries.append(' '.join(current_query))
            current_query = []
        else:
            current_query.append(line)
            
    return queries

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def estimate_query_time(connection, query):
    """Get query execution time using MySQL profiling"""
    try:
        cursor = connection.cursor()
        
        # Enable profiling
        cursor.execute("SET profiling = 1")
        
        # Execute the actual query and fetch results
        cursor.execute(query)
        if cursor.description:  # If there are results to fetch
            cursor.fetchall()
        
        # Get the profile data
        cursor.execute("SHOW PROFILES")
        profiles = cursor.fetchall()
        
        # Get the last query duration (most recent)
        if profiles:
            duration = float(profiles[-1][1])  # Duration is in the second column
            cursor.close()
            return f"{duration:.2f}s"
        
        cursor.close()
        return "0s"
        
    except Error as e:
        if cursor:
            cursor.close()
        return f"Error: {str(e)}"

def process_sql_file(connection, sql_file_path):
    try:
        results = []
        # Read and split SQL queries
        sql_content = read_sql_file(sql_file_path)
        queries = split_queries(sql_content)
        
        for i, query in enumerate(queries, 1):
            try:
                cursor = connection.cursor()
                
                print(f"\nExecuting query {i} from {sql_file_path}")
                print(f"Query: {query}")
                
                # Get execution time using profiling
                estimate_time = estimate_query_time(connection, query)
                print(f"Execution time: {estimate_time}")
                
                # Execute query again to get results
                cursor.execute(query)
                
                # Skip if query doesn't return results (e.g., SET statements)
                if not cursor.description:
                    print("Query executed successfully (no results to export)")
                    cursor.close()
                    continue
                
                # Fetch results
                records = cursor.fetchall()
                print(f"Total number of rows: {cursor.rowcount}")

                # Store results
                if records and len(records[0]) > 0:
                    count = records[0][0]  # Assuming the count is in the first column
                else:
                    count = 0
                
                results.append({
                    'id': i,
                    'sql': query,
                    'total_count': count,
                    'estimate_time': estimate_time
                })
                
                print("\nFirst few rows of data:")
                for row in records[:3]:
                    print(row)
                    
                cursor.close()
                
            except Error as e:
                print(f"Error executing query {i}: {e}")
                if cursor:
                    cursor.close()
                continue
        
        return results
            
    except Exception as e:
        print(f"Error processing {sql_file_path}: {e}")
        return []

def connect_and_query():
    try:
        # Clean estimate directory first
        clean_estimate_directory()
        
        # MySQL connection details from config
        connection = mysql.connector.connect(
            host=config['MySQL']['host'],
            port=int(config['MySQL']['port']),
            user=config['MySQL']['user'],
            password=config['MySQL']['password'],
            database=config['MySQL']['database'],
            allow_local_infile=config['MySQL'].getboolean('allow_local_infile'),
        )

        if connection.is_connected():
            # Enable profiling at connection level
            cursor = connection.cursor()
            cursor.execute("SET profiling = 1")
            cursor.close()
            
            # Ensure output directory exists
            ensure_directory_exists(OUTPUT_DIR)
            
            # Process all SQL files in the input directory
            for sql_file in os.listdir(INPUT_DIR):
                if sql_file.endswith('.sql'):
                    sql_file_path = os.path.join(INPUT_DIR, sql_file)
                    results = process_sql_file(connection, sql_file_path)
                    
                    if results:
                        # Create output filename based on SQL filename
                        base_name = os.path.splitext(sql_file)[0]
                        output_file = os.path.join(OUTPUT_DIR, f'{base_name}_count_result.csv')
                        
                        # Write results to CSV file
                        with open(output_file, 'w', newline='') as csvfile:
                            fieldnames = ['id', 'sql', 'total_count', 'estimate_time']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            for result in results:
                                writer.writerow(result)
                        
                        print(f"\nResults have been exported to {output_file}")

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("\nMySQL connection closed.")

if __name__ == "__main__":
    connect_and_query() 