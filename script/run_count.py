import subprocess
import sys
import os
import time

def run_script(script_path, args=None):
    """Run a Python script and handle any errors"""
    try:
        print(f"\nExecuting {script_path}...")
        # Create a new environment with the current environment variables
        env = os.environ.copy()
        # Ensure PYTHONPATH includes the script directory
        script_dir = os.path.dirname(script_path)
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = f"{script_dir}:{env['PYTHONPATH']}"
        else:
            env['PYTHONPATH'] = script_dir
            
        cmd = [sys.executable, script_path]
        if args:
            cmd.extend(args)
            
        # Run the script with the modified environment
        result = subprocess.run(cmd, check=True, env=env)
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
    links_file = os.path.join(os.path.dirname(script_dir), "properties", "notion_links.txt")
    
    # Step 1: Run scraper_stable.py with the correct links file path
    if not run_script(scraper_script, ['--links-file', links_file]):
        print("Failed to execute scraper_stable.py. Stopping execution.")
        return
    
    # Add a small delay to ensure all resources are properly released
    time.sleep(2)
    
    # Step 2: Run estimate_count.py
    if not run_script(estimate_script):
        print("Failed to execute estimate_count.py. Stopping execution.")
        return
    
    print("\nAll scripts completed successfully!")

if __name__ == "__main__":
    main() 