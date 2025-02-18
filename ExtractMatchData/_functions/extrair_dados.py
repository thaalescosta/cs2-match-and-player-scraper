import os
import subprocess
import time
from tqdm import tqdm  # Import tqdm for progress bar

def run_csda_on_demos(tournaments_df):
    tournaments_df['output_data_path'] = None
    print("\n---------------------------------------------")
    # Group by tournament to process each tournament's demos only once
    for tournament, group in tournaments_df.groupby('tournament'):
        # Get the first row of the group to get common paths
        row = group.iloc[0]
        csda_path = os.path.join(row['root'], r"_resources", r"csda.exe")
        demos_path = row['demo_path']
        output_path = os.path.join(row['root'], r"downloads", r"extracted_data", tournament)
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(demos_path):
            os.makedirs(demos_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Get the list of .dem files
        dem_files = [f for f in os.listdir(demos_path) if f.endswith('.dem')]
        
        print(f"\nNumber of games: {len(dem_files)}")
        
        # Iterate over all .dem files with a progress bar
        for filename in tqdm(dem_files,
                        desc=f"Processing {tournament}",
                        maxinterval=1.0,
                        unit="file",
                        ncols=100,  # Adjust the width of the progress bar
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]"
                        ):
            # Construct the full path to the .dem file
            # If demos_path is "c:\cs2-hltv-event-scrapper\ExtractMatchData\downloads\unpacked_demos\BLAST Bounty 2025 Season 1 Finals"
            # and filename is "game.dem"
            # dem_path would be "c:\cs2-hltv-event-scrapper\ExtractMatchData\downloads\unpacked_demos\BLAST Bounty 2025 Season 1 Finals\game.dem"
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

        # Update output_data_path for all matches in this tournament
        tournaments_df.loc[tournaments_df['tournament'] == tournament, 'output_data_path'] = output_path
        
    return tournaments_df