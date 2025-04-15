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
            'event_id': event_id,
            'match_id': match_id,
            'map_n': map_number,
            'p': p_value,
            'demo_filename': dem_file
        }
    except Exception as e:
        print(f"Error processing {dem_file}: {e}")
        return None

def unrar(tournaments_df: pd.DataFrame) -> pd.DataFrame:
    root_path = tournaments_df.iloc[0]['root']
    rarfile.UNRAR_TOOL = os.path.join(root_path, "_resources", "UnRAR.exe")
    source_folder = os.path.join(root_path, "downloads", 'demos')

    rar_files = [f for f in os.listdir(source_folder) if f.endswith('.rar')]
    print(f"Total .rar files to extract: {len(rar_files)}")
    print("Starting extraction...", flush=True)
    
    if not rar_files:
        print("No .rar files found for extraction.")
        return tournaments_df

    destinations = set()
    all_dem_info = []

    for rar_filename in rar_files:
        print(f"Extracting: {rar_filename}")
        
        event_id = extract_file_info(rar_filename, r'E(\d+)_')
        match_id = extract_file_info(rar_filename, r'M(\d+)_')
        
        if not all([event_id, match_id]):
            print(f"Could not find event/match ID in filename: {rar_filename}")
            continue

        match = tournaments_df[(tournaments_df['event_id'] == event_id) & 
                             (tournaments_df['match_id'] == match_id)]
        
        if match.empty:
            continue

        tournament = match['tournament'].values[0]
        destination_folder = os.path.join(root_path, "downloads", 'unpacked_demos', tournament)
        os.makedirs(destination_folder, exist_ok=True)
        destinations.add(destination_folder)

        rar_path = os.path.join(source_folder, rar_filename)
        
        try:
            # First check if the file exists and is accessible
            if not os.path.exists(rar_path):
                print(f"RAR file not found: {rar_path}")
                continue
                
            # Try to open the RAR file
            with rarfile.RarFile(rar_path) as rf:
                # Extract all files
                rf.extractall(destination_folder)
                
                # Process extracted .dem files
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

        except rarfile.RarCannotExec as e:
            print(f"Error extracting {rar_filename}: {e}. Ensure 'unrar' is installed and accessible.")
        except rarfile.BadRarFile as e:
            print(f"Bad RAR file {rar_filename}: {e}")
        except Exception as e:
            print(f"An error occurred with {rar_filename}: {e}")

        tournaments_df.loc[
            (tournaments_df['event_id'] == event_id) & 
            (tournaments_df['match_id'] == match_id), 
            'demo_path'
        ] = destination_folder

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
        tournaments_df = pd.merge(
            tournaments_df,
            dem_info,
            on=['event_id', 'match_id', 'map_n'],
            how='left'
        )

    return tournaments_df
