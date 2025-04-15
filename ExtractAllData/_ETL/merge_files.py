import os
import pandas as pd
import shutil

def merge_csv_files(tournaments_df):
    # Verify required columns exist
    required_columns = ['tournament', 'output_data_path', 'match_id']
    missing_columns = [col for col in required_columns if col not in tournaments_df.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns in tournaments_df: {missing_columns}")

    files = [
        "_clutches.csv",
        "_kills.csv",
        "_match.csv",
        "_players.csv",
        "_players_economy.csv",
        "_rounds.csv",
        "_teams.csv"
    ]
    # Dictionary to store combined DataFrames for all tournaments
    all_tournaments_data = {suffix.replace('.csv',''): [] for suffix in files}
    
    # Group by tournament to process each tournament's data separately
    for tournament, group in tournaments_df.groupby('tournament'):
        output_path = group.iloc[0]['output_data_path']
        
        # Get all CSV files in the folder
        all_files = pd.Series([f for f in os.listdir(output_path) if f.endswith(".csv")])
        
        for suffix in files:
            # Filter files that match the current suffix
            matching_files = all_files[all_files.str.endswith(suffix)]
            
            if matching_files.empty:
                continue
            
            # Read and concatenate all matching files
            dfs = [pd.read_csv(os.path.join(output_path, f)) for f in matching_files]
            merged_df = pd.concat(dfs, ignore_index=True)
            
            # Clean up column names
            merged_df.columns = merged_df.columns.str.replace(" ", "_")
            
            # Special handling for specific files
            if suffix == "_teams.csv":
                merged_df.columns = merged_df.columns.str.replace(" ", "_")
                merged_df.rename(columns={"letter": "team"}, inplace=True)
                merged_df["team"].replace({"A": "Team A", "B": "Team B"})
            
            elif suffix == "_clutches.csv":
                merged_df.columns = merged_df.columns.str.replace(" ", "_")
                merged_df.rename(columns={'match_checksum': 'checksum', 'side': 'player_side'}, inplace=True)
                merged_df["player_side"].replace({3: "Counter Terrorist", 2: "Terrorist"})

            elif suffix == "_players_economy.csv":
                merged_df.columns = merged_df.columns.str.replace(" ", "_")
                merged_df["player_side"].replace({3: "Counter Terrorist", 2: "Terrorist"})
            
            elif suffix == "_rounds.csv":
                merged_df.columns = merged_df.columns.str.replace(" ", "_")
                merged_df["winner_side"].replace({3: "Counter Terrorist", 2: "Terrorist"})
            
            elif suffix == "_players.csv":
                merged_df.columns = merged_df.columns.str.replace(" ", "_")
                merged_df.rename(columns={'k/d': 'kd', 'hs_%': 'hs_percentage', '1k' : 'k_1', '2k' : 'k_2', '3k' : 'k_3', '4k' : 'k_4', '5k' : 'k_5'  }, inplace=True)
            
            elif suffix == "_kills.csv":
                merged_df.columns = merged_df.columns.str.replace(" ", "_")
                merged_df.rename(columns={'k/d': 'kd', 'hs_%': 'hs_percentage', '1k' : 'k_1', '2k' : 'k_2', '3k' : 'k_3', '4k' : 'k_4', '5k' : 'k_5'  }, inplace=True)
                merged_df["victim_side"].replace({3: "Counter Terrorist", 2: "Terrorist"})
            
            elif suffix == "_match.csv":
                merged_df.columns = merged_df.columns.str.replace(" ", "_")
                merged_df["date"] = pd.to_datetime(merged_df["date"]).dt.date
                merged_df["match_id"] = tournaments_df.loc[tournaments_df['tournament'] == tournament, 'match_id'].iloc[0]
                # Create unique_name without relying on tournament column in merged_df
                merged_df["unique_name"] = merged_df["demo_name"] + "_" + tournament.lower().replace(" ", "-")
            
            # Add to all tournaments data
            all_tournaments_data[suffix.replace('.csv','')].append(merged_df)
    
    # Only drop columns that exist
    columns_to_drop = {'Unnamed: 0', 'root', 'url_request', 'direct_url_demo', 'file_name', 'demo_path', 'output_data_path'}
    existing_columns = [col for col in columns_to_drop if col in tournaments_df.columns]
    if existing_columns:
        tournaments_df.drop(columns=existing_columns, inplace=True)
    
    #Combine all tournaments data
    return {name: pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame() 
            for name, dfs in all_tournaments_data.items()}
