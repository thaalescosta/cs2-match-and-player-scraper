import os
import rarfile
import re
import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path

def extract_file_info(filename: str, pattern: str) -> Optional[int]:
    match = re.search(pattern, filename)
    return int(match.group(1)) if match else None

def process_dem_file(dem_file: str) -> Optional[Dict]:
    try:
        map_match = re.search(r'-m(\d+)-', dem_file)
        map_number = f"m{map_match.group(1)}" if map_match else None
        
        event_id = extract_file_info(dem_file, r'E(\d+)_')
        match_id = extract_file_info(dem_file, r'M(\d+)_')
        
        p_match = re.search(r'p(\d+)\.dem', dem_file)
        p_value = p_match.group(1) if p_match else None

        return {
            'event_id': str(event_id),  # Convert to string to match tournaments_df type
            'match_id': str(match_id),  # Convert to string to match tournaments_df type
            'map_n': map_number,
            'p': p_value,
            'demo_filename': dem_file
        }
    except Exception as e:
        print(f"Error processing {dem_file}: {e}")
        return None

def unrar(tournaments_df):
    root_path = tournaments_df.iloc[0]['root']
    rarfile.UNRAR_TOOL = os.path.join(root_path, r"_resources", r"UnRAR.exe")  # Fixed case sensitivity
    source_folder = os.path.join(root_path, r"downloads", r"demos")
    
    rar_files = [f for f in os.listdir(source_folder) if f.endswith('.rar')]
    # print(f"Total .rar files to extract: {len(rar_files)}")
    # print("Starting extraction...", flush=True)
    
    if not rar_files:
        print("No .rar files found for extraction.")
        return tournaments_df

    destinations = set()
    all_dem_info = []

    from tqdm import tqdm

    for rar_filename in tqdm(rar_files, unit="file", desc="Extracting RAR files"):
        # Find the first matching tournament value for the .rar file
        row = tournaments_df[tournaments_df['file_name'] == rar_filename].iloc[0]
        
        tournament = row['tournament']  # Get the tournament value
        destination_folder = os.path.join(tournaments_df.iloc[0]['root'], r"downloads", r'unpacked_demos', tournament)

        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        rar_path = os.path.join(source_folder, rar_filename)

        try:
            event_id = str(extract_file_info(rar_filename, r'E(\d+)_'))  # Convert to string
            match_id = str(extract_file_info(rar_filename, r'M(\d+)_'))  # Convert to string
            
            if not all([event_id, match_id]):
                print(f"Could not find event/match ID in filename: {rar_filename}")
                continue

            os.makedirs(destination_folder, exist_ok=True)
            destinations.add(destination_folder)

            rar_path = os.path.join(source_folder, rar_filename)
            
            # First check if the file exists and is accessible
            if not os.path.exists(rar_path):
                print(f"RAR file not found: {rar_path}")
                continue
                
            # print(f"Extracting {rar_filename} to {destination_folder}")
            rf = rarfile.RarFile(rar_path)
            rf.extractall(destination_folder)

            extracted_files = [f for f in os.listdir(destination_folder) if f.endswith('.dem')]
            if not extracted_files:
                print(f"No .dem files found in {rar_filename}")
                continue
                
            for dem_file in extracted_files:
                if not re.match(r'^E\d+_M\d+_', dem_file):
                    old_path = os.path.join(destination_folder, dem_file)
                    new_name = f"E{event_id}_M{match_id}_{dem_file}"
                    new_path = os.path.join(destination_folder, new_name)
                    os.rename(old_path, new_path)
                    
            # Verify extraction was successful
            if not any(f.endswith('.dem') for f in os.listdir(destination_folder)):
                print(f"Warning: No .dem files found after extraction in {destination_folder}")

            tournaments_df.loc[
                (tournaments_df['event_id'].astype(str) == event_id) & 
                (tournaments_df['match_id'].astype(str) == match_id), 
                'demo_path'
            ] = destination_folder

        except Exception as e:
            print(f"Error processing {rar_filename}: {e}")
            continue

    # Process all extracted dem files
    for destination_folder in destinations:
        dem_files = [f for f in os.listdir(destination_folder) if f.endswith('.dem')]
        if not dem_files:
            print(f"Warning: No .dem files found in {destination_folder}")
            continue
            
        for dem_file in dem_files:
            if dem_info := process_dem_file(dem_file):
                all_dem_info.append(dem_info)

    dem_info = pd.DataFrame(all_dem_info) if all_dem_info else pd.DataFrame()
    if not dem_info.empty:
        # Convert event_id and match_id to string in tournaments_df for consistent merging
        tournaments_df['event_id'] = tournaments_df['event_id'].astype(str)
        tournaments_df['match_id'] = tournaments_df['match_id'].astype(str)
        
        tournaments_df = pd.merge(
            tournaments_df,
            dem_info,
            on=['event_id', 'match_id', 'map_n'],
            how='left'
        )

    return tournaments_df
