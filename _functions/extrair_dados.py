import os
import subprocess
import time
from tqdm import tqdm  # Import tqdm for progress bar

def run_csda_on_demos(csda_path, demos_path, output_path, camp):
    print()
    # Create the output directory if it doesn't exist
    if not os.path.exists(demos_path):
        os.makedirs(demos_path)
    output_path = os.path.join(output_path, camp)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Get the list of .dem files
    dem_files = [f for f in os.listdir(demos_path) if f.endswith('.dem')]

    # Iterate over all .dem files with a progress bar
    for filename in tqdm(dem_files, desc="Processing Demos", unit="file"):
        # Construct the full path to the .dem file
        dem_path = os.path.join(demos_path, filename)
        
        # Construct the command to run csda (as a single string for shell=True)
        sources = ["esl", "faceit", "valve"]
        for source in sources:
            command = f"""\"{csda_path}\" -demo-path=\"{dem_path}\" -output=\"{output_path}\" -source=\"{source}\" > nul"""
            try:
                # Run the command with shell=True
                subprocess.run(command, shell=True, check=True)
                break  # If the command succeeds, break out of the loop
            except subprocess.CalledProcessError as e:
                if "unknown demo source" in str(e):
                    print(f"Unknown demo source for {filename} with source {source}, trying next source...")
                    continue  # Try the next source
                else:
                    print(f"Error processing {filename}: {e}")
                    break  # If it's a different error, break out of the loop
            except Exception as e:
                print(f"An unexpected error occurred with {filename}: {e}")
                break  # Break out of the loop for any other exceptions
        time.sleep(2)

    print(f"\n\nAll data from {camp} has been exported to CSV.")