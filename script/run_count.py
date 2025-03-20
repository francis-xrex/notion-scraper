import subprocess
import sys
import os

def run_script(script_path, args=None):
    """Run a Python script and handle any errors"""
    try:
        print(f"\nExecuting {script_path}...")
        cmd = [sys.executable, script_path]
        if args:
            cmd.extend(args)
        result = subprocess.run(cmd, check=True)
        print(f"Successfully completed {script_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}")
        return False

def main():
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths to the scripts
    scraper_script = os.path.join(script_dir, "scraper_stable.py")
    estimate_script = os.path.join(script_dir, "estimate_count.py")
    links_file = os.path.join(script_dir, "notion_links.txt")
    
    # Step 1: Run scraper_stable.py with the correct links file path
    if not run_script(scraper_script, ['--links-file', links_file]):
        print("Failed to execute scraper_stable.py. Stopping execution.")
        return
    
    # Step 2: Run estimate_count.py
    if not run_script(estimate_script):
        print("Failed to execute estimate_count.py. Stopping execution.")
        return
    
    print("\nAll scripts completed successfully!")

if __name__ == "__main__":
    main() 