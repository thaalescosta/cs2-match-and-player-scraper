import os
import pandas as pd
import shutil

def merge_csv_files(tournaments_df):
    columns_to_drop = {
        "_clutches.csv": ["frame", "tick", "source_file", "opponents", "side"],
        "_kills.csv": ["frame", "tick", "round", "killer_side", "assister_name", "assister_steamid", "assister_side", "assister_team_name", "weapon_type", "penetrated_objects", "is_flash_assist", "killer_controlling_bot", "victim_controlling_bot", "assister_controlling_bot", "killer_x", "killer_y", "killer_z", "is_killer_airborne", "is_killer_blinded", "victim_x", "victim_y", "victim_z", "is_victim_airborne", "is_victim_blinded", "is_victim_inspecting_weapon", "assister_x", "assister_y", "assister_z", "is_trade_death", "is_through_smoke", "is_no_scope", "distance", "source_file"],
        "_match.csv": ["game", "demo_path", "demo_name", "type", "share_code", "server_name", "client_name", "tick_count", "tickrate", "framerate", "game_type", "game_mode", "game_mode_str", "is_ranked", "duration", "network_protocol", "build_number", "shot_count", "winner_name", "winner_side", "overtime_count", "max_rounds", "has_vac_live_ban"],
        "_players.csv": ["score", "mvp", "rank_type", "rank", "old_rank", "bomb_planted", "bomb_defused", "hostage_rescued", "1v1", "1v2", "1v3", "1v4", "1v5", "1v1_won", "1v2_won", "1v3_won", "1v4_won", "1v5_won", "1v1_lost", "1v2_lost", "1v3_lost", "1v4_lost", "1v5_lost", "color", "inspect_weapon_count", "source_file"],
        "_players_economy.csv": ["start_money", "money_spent", "source_file"],
        "_teams.csv": ["score", "score_first_half", "score_second_half", "current_side"]
    }
    # Dictionary to store combined DataFrames for all tournaments
    all_tournaments_data = {suffix.replace('.csv',''): [] for suffix in columns_to_drop.keys()}
    
    # Group by tournament to process each tournament's data separately
    for tournament, group in tournaments_df.groupby('tournament'):
        output_path = group.iloc[0]['output_data_path']
        
        # Get all CSV files in the folder
        all_files = pd.Series([f for f in os.listdir(output_path) if f.endswith(".csv")])
        
        for suffix, column in columns_to_drop.items():
            # Filter files that match the current suffix
            matching_files = all_files[all_files.str.endswith(suffix)]
            
            if matching_files.empty:
                continue
            
            # Read and concatenate all matching files
            dfs = [pd.read_csv(os.path.join(output_path, f)) for f in matching_files]
            merged_df = pd.concat(dfs, ignore_index=True)
            
            # Clean up column names
            merged_df.columns = merged_df.columns.str.replace(" ", "_")
            
            # Add tournament column for all data
            merged_df["tournament"] = tournament
            
            # Drop specified columns
            merged_df.drop(columns=[col for col in column if col in merged_df.columns], 
                         inplace=True, errors='ignore')
            
            # Special handling for specific files
            if suffix == "_teams.csv":
                merged_df.rename(columns={"letter": "team"}, inplace=True)
                merged_df["team"] = merged_df["team"].replace({"A": "Team A", "B": "Team B"})
            
            elif suffix == "_players_economy.csv":
                merged_df["player_side"] = merged_df["player_side"].replace({3: "Counter Terrorist", 2: "Terrorist"})
            
            elif suffix == "_players.csv":
                merged_df = merged_df.rename(columns={'k/d': 'kd'})
            
            elif suffix == "_kills.csv":
                merged_df["victim_side"] = merged_df["victim_side"].replace({3: "Counter Terrorist", 2: "Terrorist"})
            
            elif suffix == "_match.csv":
                merged_df["date"] = pd.to_datetime(merged_df["date"]).dt.date
            
            # Add to all tournaments data
            all_tournaments_data[suffix.replace('.csv','')].append(merged_df)
    
    if os.path.exists(os.path.join(tournaments_df.iloc[0]['root'], 'downloads')):
        shutil.rmtree(os.path.join(tournaments_df.iloc[0]['root'], 'downloads')) 
    
    tournaments_df['event_id'] = None
    tournaments_df = tournaments_df.drop(columns={'root', 'url_request', 'direct_url_demo', 'file_name'}, inplace=True)
      
    #Combine all tournaments data
    return {name: pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame() 
            for name, dfs in all_tournaments_data.items()}

