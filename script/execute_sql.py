import os
import sys
import mysql.connector
from mysql.connector import Error
import glob
import configparser
from datetime import datetime

def read_credentials():
    """Read database credentials and directory paths from config.properties file"""
    credentials = {}
    try:
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'properties', 'config.properties')
        config.read(config_path)
        
        # Read MySQL section
        credentials['host'] = config.get('MySQL', 'host')
        credentials['port'] = config.get('MySQL', 'port')
        credentials['user'] = config.get('MySQL', 'user')
        credentials['password'] = config.get('MySQL', 'password')
        credentials['database'] = config.get('MySQL', 'database')
        
        # Read Directories section
        credentials['delete_ky_dir'] = config.get('Directories', 'delete_ky_dir')
        credentials['delete_tw_dir'] = config.get('Directories', 'delete_tw_dir')
        
    except Exception as e:
        print(f"Error reading config.properties: {e}")
        sys.exit(1)
    return credentials

def log_error(sql_file, error_message):
    """Log error to a file named after the SQL file"""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    sql_filename = os.path.basename(sql_file)
    log_filename = f"{os.path.splitext(sql_filename)[0]}_error.log"
    log_path = os.path.join(log_dir, log_filename)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, 'a') as f:
        f.write(f"[{timestamp}] Error executing {sql_filename}:\n{error_message}\n\n")

def execute_sql_file(cursor, sql_file):
    """Execute a SQL file"""
    try:
        # Add confirmation prompt
        sql_filename = os.path.basename(sql_file)
        confirmation = input(f"Do you want to execute {sql_filename}? (yes/no): ").lower()
        if confirmation != 'yes':
            print(f"Skipping {sql_filename}")
            return True

        # Disable safe updates mode
        cursor.execute("SET SQL_SAFE_UPDATES = 0;")

        with open(sql_file, 'r') as f:
            sql_commands = f.read()
            
        # Split the SQL commands by semicolon
        for command in sql_commands.split(';'):
            if command.strip():
                print(f"Executing SQL from {sql_filename}...")
                cursor.execute(command)
                
                # Fetch results if it's a SELECT query
                if command.strip().upper().startswith('SELECT'):
                    results = cursor.fetchall()
                    print(f"Query results: {results}")
                
                print(f"Successfully executed SQL from {sql_filename}")
                
    except Error as e:
        error_message = f"Error executing SQL file {sql_file}: {e}"
        print(error_message)
        log_error(sql_file, error_message)
        return False
    return True

def main():
    # Read database credentials and directory paths
    credentials = read_credentials()
    delete_ky_dir = credentials['delete_ky_dir']
    delete_tw_dir = credentials['delete_tw_dir']
    
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host=credentials.get('host'),
            port=int(credentials.get('port')),
            user=credentials.get('user'),
            password=credentials.get('password'),
            database=credentials.get('database')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Process delete_ky directory first
            print("\nProcessing delete_ky directory...")
            sql_files_ky = glob.glob(os.path.join(delete_ky_dir, "*.sql"))
            if not sql_files_ky:
                print(f"No SQL files found in {delete_ky_dir}")
            else:
                for sql_file in sql_files_ky:
                    if not execute_sql_file(cursor, sql_file):
                        print(f"Failed to execute {sql_file}")
                        continue
            
            # Process delete_tw directory
            print("\nProcessing delete_tw directory...")
            sql_files_tw = glob.glob(os.path.join(delete_tw_dir, "*.sql"))
            if not sql_files_tw:
                print(f"No SQL files found in {delete_tw_dir}")
            else:
                for sql_file in sql_files_tw:
                    if not execute_sql_file(cursor, sql_file):
                        print(f"Failed to execute {sql_file}")
                        continue
                
            # Commit all changes
            connection.commit()
            print("\nAll SQL files executed successfully!")
            
    except Error as e:
        print(f"Error connecting to database: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main() 