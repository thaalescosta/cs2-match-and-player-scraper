import os
import subprocess
import time
import pandas as pd
from tqdm import tqdm  # Import tqdm for progress bar

def run_csda_on_demos(tournaments_df):
    # Initialize required columns if they don't exist
    if 'output_data_path' not in tournaments_df.columns:
        tournaments_df['output_data_path'] = None
    if 'checksum' not in tournaments_df.columns:
        tournaments_df['checksum'] = None
    if 'demo_path' not in tournaments_df.columns:
        tournaments_df['demo_path'] = None
    if 'demo_filename' not in tournaments_df.columns:
        tournaments_df['demo_filename'] = None
    
    print("\n---------------------------------------------")
    # Group by tournament to process each tournament's demos only once
    for tournament, group in tournaments_df.groupby('tournament'):
        # Get the first row of the group to get common paths
        row = group.iloc[0]
        csda_path = os.path.join(row['root'], r"_resources", r"csda.exe")
        output_path = os.path.join(row['root'], r"downloads", r"extracted_data", tournament)
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Create a set to track processed checksums at the tournament level
        tournament_processed_checksums = set()
        
        # Iterate over all demos in the group with a progress bar
        for _, demo_row in tqdm(group.iterrows(),
                        desc=f"Processing {tournament}",
                        total=len(group),
                        unit="file",
                        ncols=100,
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]"
                        ):
            if pd.isna(demo_row['demo_path']) or pd.isna(demo_row['demo_filename']):
                continue
                
            # Construct the full path to the .dem file
            dem_path = os.path.join(demo_row['demo_path'], demo_row['demo_filename'])
            
            sources = ["esl", "faceit", "valve"]
            success = False
            for source in sources:
                command = f"""\"{csda_path}\" -demo-path=\"{dem_path}\" -output=\"{output_path}\" -source=\"{source}\" > nul"""
                try:
                    # Run the command with shell=True
                    subprocess.run(command, shell=True, check=True)
                    success = True
                    break  # If the command succeeds, break out of the loop
                except subprocess.CalledProcessError as e:
                    if "unknown demo source" in str(e):
                        print(f"Unknown demo source for {demo_row['demo_filename']} with source {source}, trying next source...")
                        continue  # Try the next source
                    else:
                        print(f"Error processing {demo_row['demo_filename']}: {e}")
                        break  # If it's a different error, break out of the loop
                except Exception as e:
                    print(f"An unexpected error occurred with {demo_row['demo_filename']}: {e}")
                    break  # Break out of the loop for any other exceptions

            if not success:
                continue  # Skip to next file if processing failed

            # List of files to keep
            keep_suffixes = [
                "_clutches.csv",
                "_kills.csv",
                "_match.csv",
                "_players.csv",
                "_players_economy.csv",
                "_rounds.csv",
                "_teams.csv"
            ]
            
            # Get all CSV files in the output directory
            all_csv_files = [f for f in os.listdir(output_path) if f.endswith('.csv')]
            
            # Delete files that don't match the keep suffixes
            for csv_file in all_csv_files:
                if not any(csv_file.endswith(suffix) for suffix in keep_suffixes):
                    file_path = os.path.join(output_path, csv_file)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting file {csv_file}: {e}")

            # Find all match CSV files
            match_csvs = [f for f in os.listdir(output_path) if f.endswith('_match.csv')]
            
            for match_csv in match_csvs:
                # Read the match CSV file
                match_df = pd.read_csv(os.path.join(output_path, match_csv))
                # Extract checksum from the CSV
                checksum = match_df['checksum'].iloc[0]
                
                # Only process and print if we haven't seen this checksum before
                if checksum not in tournament_processed_checksums:
                    # Update the DataFrame where the filename is in the match CSV filename
                    mask = tournaments_df['demo_filename'].str.replace('.dem', '').str.contains(match_csv.replace('_match.csv', ''), case=False, na=False)

                    tournaments_df.loc[mask, 'checksum'] = checksum
                    
                    # Add to processed set
                    tournament_processed_checksums.add(checksum)

            time.sleep(1)

        tournaments_df.loc[tournaments_df['tournament'] == tournament, 'output_data_path'] = output_path

    return tournaments_df