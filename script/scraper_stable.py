from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
import time
import os
from datetime import datetime
import argparse
from dotenv import load_dotenv
import configparser
import shutil

# Load environment variables from script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)  # Get the parent directory (count_result)
env_path = os.path.join(parent_dir, 'properties', 'credentials.properties')
config_path = os.path.join(parent_dir, 'properties', 'config.properties')

def cleanup_directories():
    """Clean up all files in the specified directories"""
    directories = [
        config.get('Directories', 'count_tw_dir'),
        config.get('Directories', 'count_ky_dir'),
        config.get('Directories', 'delete_tw_dir'),
        config.get('Directories', 'delete_ky_dir')
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"Cleaning up directory: {directory}")
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        else:
            print(f"Directory does not exist: {directory}")

# Load configurations
config = configparser.ConfigParser()
config.read(config_path)

# Load environment variables
load_dotenv(env_path)

class NotionScraper:
    def __init__(self):
        """Initialize the Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        # Load output directories from config
        self.count_tw_dir = config.get('Directories', 'count_tw_dir')
        self.count_ky_dir = config.get('Directories', 'count_ky_dir')
        self.delete_tw_dir = config.get('Directories', 'delete_tw_dir')
        self.delete_ky_dir = config.get('Directories', 'delete_ky_dir')
        print(f"Using count TW directory: {self.count_tw_dir}")
        print(f"Using count KY directory: {self.count_ky_dir}")
        print(f"Using delete TW directory: {self.delete_tw_dir}")
        print(f"Using delete KY directory: {self.delete_ky_dir}")

    def login_with_google(self, email, password):
        """Login to Notion using Google"""
        try:
            print("Logging in to Notion with Google...")
            self.driver.get('https://www.notion.so/login')
            time.sleep(3)

            # Click "Continue with Google"
            print("Clicking 'Continue with Google'...")
            google_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Continue with Google')]"))
            )
            google_button.click()
            time.sleep(1)

            # Switch to Google login window
            print("Switching to Google login window...")
            windows = self.driver.window_handles
            if len(windows) < 2:
                print("Error: Google login window not opened")
                return False
            self.driver.switch_to.window(windows[-1])
            time.sleep(3)

            # Enter email
            print("Entering email...")
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
            )
            email_input.clear()
            for char in email:
                email_input.send_keys(char)
                time.sleep(0.1)
            time.sleep(1)
            email_input.send_keys(Keys.RETURN)
            time.sleep(5)

            # Enter password
            print("Entering password...")
            try:
                password_input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
                )
            except:
                try:
                    password_input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
                    )
                except:
                    print("Could not find password input field")
                    return False
            
            password_input.clear()
            for char in password:
                password_input.send_keys(char)
                time.sleep(0.1)
            time.sleep(1)
            password_input.send_keys(Keys.RETURN)
            time.sleep(2)

            # Check for 2FA prompt
            try:
                twofa_input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="tel"]'))
                )
                if twofa_input:
                    print("\nTwo-factor authentication required!")
                    print("Please check your authentication app or SMS and enter the code:")
                    code = input().strip()
                    for char in code:
                        twofa_input.send_keys(char)
                        time.sleep(0.1)
                    twofa_input.send_keys(Keys.RETURN)
                    time.sleep(8)
            except TimeoutException:
                print("No 2FA prompt detected")
            except Exception as e:
                print(f"Error during 2FA: {e}")
                return False

            # Switch back to Notion window
            print("Switching back to Notion...")
            self.driver.switch_to.window(windows[0])
            time.sleep(1)

            # Wait for Notion to load and redirect to XREX Headquarters
            print("Redirecting to XREX Headquarters...")
            self.driver.get('https://www.notion.so/xrexuiux/XREX-Headquarters-8d9c1fc2cf394708baeabf1852fa2c3e')
            time.sleep(3)  # Wait longer for the page to load

            # Check if we're on the correct page
            current_url = self.driver.current_url
            if 'XREX-Headquarters' in current_url:
                print("Successfully redirected to XREX Headquarters")
                return True
            else:
                print(f"Failed to reach XREX Headquarters. Current URL: {current_url}")
                return False

        except Exception as e:
            print(f"Error during Google login: {e}")
            print("Current URL:", self.driver.current_url)
            return False

    def close(self):
        """Close the browser"""
        self.driver.quit()

    def extract_content_between_markers(self, full_content, start_marker, end_marker):
        """Extract content between given markers"""
        try:
            start_idx = full_content.index(start_marker) + len(start_marker)
            end_idx = full_content.index(end_marker)
            return full_content[start_idx:end_idx].strip()
        except ValueError:
            print(f"Could not find markers {start_marker} and {end_marker}")
            return None

    def scrape_page(self, page_url, page_name):
        """Scrape raw content from a Notion page and save to separate files"""
        try:
            print(f"Accessing page: {page_url}")
            self.driver.get(page_url)
            
            # Wait for the main content to load
            print("Waiting for content to load...")
            main_content = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="notion-page-content"]'))
            )

            # Wait a bit for dynamic content
            time.sleep(5)
            print("Extracting content...")
            
            # Get all text blocks
            text_blocks = self.driver.find_elements(By.CSS_SELECTOR, '[class*="notion-text-block"], [class*="notion-code-block"]')
            
            # Extract raw text and use a set to deduplicate
            content_set = set()
            for block in text_blocks:
                text = block.text.strip()
                if text:
                    content_set.add(text)
            
            # Join all content
            full_content = '\n\n'.join(sorted(content_set))
            
            # Extract content between markers
            tw_content = self.extract_content_between_markers(full_content, "#count_tw_start", "#count_tw_end")
            ky_content = self.extract_content_between_markers(full_content, "#count_ky_start", "#count_ky_end")
            clean_tw_content = self.extract_content_between_markers(full_content, "#clean_tw_start", "#clean_tw_end")
            clean_ky_content = self.extract_content_between_markers(full_content, "#clean_ky_start", "#clean_ky_end")
            
            # Generate timestamp for filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create output directories if they don't exist
            os.makedirs(self.count_tw_dir, exist_ok=True)
            os.makedirs(self.count_ky_dir, exist_ok=True)
            os.makedirs(self.delete_tw_dir, exist_ok=True)
            os.makedirs(self.delete_ky_dir, exist_ok=True)
            
            # Save TW content
            if tw_content:
                tw_filename = os.path.join(self.count_tw_dir, f"{page_name}_count_tw_{timestamp}.sql")
                with open(tw_filename, 'w', encoding='utf-8') as f:
                    f.write(tw_content)
                print(f"\nTW content saved to: {tw_filename}")
            
            # Save KY content
            if ky_content:
                ky_filename = os.path.join(self.count_ky_dir, f"{page_name}_count_ky_{timestamp}.sql")
                with open(ky_filename, 'w', encoding='utf-8') as f:
                    f.write(ky_content)
                print(f"\nKY content saved to: {ky_filename}")

            # Save clean TW content
            if clean_tw_content:
                clean_tw_filename = os.path.join(self.delete_tw_dir, f"{page_name}_clean_tw_{timestamp}.sql")
                with open(clean_tw_filename, 'w', encoding='utf-8') as f:
                    f.write(clean_tw_content)
                print(f"\nClean TW content saved to: {clean_tw_filename}")
            
            # Save clean KY content
            if clean_ky_content:
                clean_ky_filename = os.path.join(self.delete_ky_dir, f"{page_name}_clean_ky_{timestamp}.sql")
                with open(clean_ky_filename, 'w', encoding='utf-8') as f:
                    f.write(clean_ky_content)
                print(f"\nClean KY content saved to: {clean_ky_filename}")
            
            return True

        except Exception as e:
            print(f"Error scraping page: {e}")
            return False

def main():
    # Clean up directories at the start
    cleanup_directories()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Scrape content from Notion pages')
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the parent directory (count_result)
    parser.add_argument('--links-file', '-f', default=os.path.join(parent_dir, 'properties', 'notion_links.txt'), help='File containing Notion page URLs')
    args = parser.parse_args()

    # Get credentials from environment variables
    email = os.getenv('GOOGLE_EMAIL')
    password = os.getenv('GOOGLE_PASSWORD')

    if not email or not password:
        print("Error: GOOGLE_EMAIL and GOOGLE_PASSWORD must be set in .env file")
        return

    scraper = NotionScraper()
    
    try:
        # Login with credentials from environment variables
        if not scraper.login_with_google(email, password):
            print("Failed to login. Please check your credentials in .env file.")
            return
        
        # Read URLs from file
        try:
            with open(args.links_file, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: Links file '{args.links_file}' not found")
            return
        
        # Process each URL
        for line in lines:
            # Split line into name and URL
            try:
                page_name, url = line.split(':', 1)
                # Remove @ symbol if present
                url = url.lstrip('@')
                print(f"\nProcessing {page_name}: {url}")
                if scraper.scrape_page(url, page_name):
                    print(f"Successfully scraped content from {page_name}")
                else:
                    print(f"Failed to scrape content from {page_name}")
            except ValueError:
                print(f"Invalid line format: {line}")
                continue
        
    finally:
        scraper.close()

if __name__ == "__main__":
    main() 