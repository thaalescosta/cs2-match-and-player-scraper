import os
import pandas as pd

def merge_csv_files(camp, camp_var, output_path, tabelas_finais):
    # Ensure the output folder exists
    output_path = os.path.join(output_path, camp)
    # List of suffixes to merge and columns to drop
    suffixes_to_drop = {
        "_clutches.csv": ["frame", "tick", "source_file", "round", "opponents", "side"],
        "_kills.csv": ["frame", "tick", "round", "killer_side", "assister_name", "assister_steamid", "assister_side", "assister_team_name", "weapon_type", "penetrated_objects", "is_flash_assist", "killer_controlling bot", "victim_controlling_bot", "assister_controlling_bot", "killer_x", "killer_y", "killer_z", "is_killer_airborne", "is_killer_blinded", "victim_x", "victim_y", "victim_z", "is_victim_airborne", "is_victim_blinded", "is_victim_inspecting_weapon", "assister_x", "assister_y", "assister_z", "is_trade_death", "is_through_smoke", "is_no_scope", "distance", "source_file"],
        "_match.csv": ["game", "demo_path", "demo_name", "source", "type", "share_code", "server_name", "client_name", "tick_count", "tickrate", "framerate", "game_type", "game_mode", "game_mode_str", "is_ranked", "duration", "network_protocol", "build_number", "kill_count", "assist_count", "death_count", "shot_count", "winner_name", "winner_side", "overtime_count", "max_rounds", "has_vac_live_ban", "source_file"],
        "_players.csv": ["score", "mvp", "rank_type", "rank", "old_rank", "win_count", "bomb_planted", "bomb_defused", "hostage_rescued", "1v1", "1v2", "1v3", "1v4", "1v5", "1v1_won", "1v2_won", "1v3_won", "1v4_won", "1v5_won", "1v1_lost", "1v2_lost", "1v3_lost", "1v4_lost", "1v5_lost", "first_trade_kill", "first_trade_death", "htlv_2", "htlv", "crosshair_share_code", "color", "inspect_weapon_count", "source_file"],
        "_players_economy.csv": ["start_money", "money_spent", "round", "source_file"],
        "_teams.csv": ["score", "score_first_half", "score_second_half", "current_side", "source_file"]
    }
    
    # Get all CSV files in the folder
    all_files = [f for f in os.listdir(output_path) if f.endswith(".csv")]
    
    for suffix in suffixes_to_drop.keys():
        # Filter files that match the current suffix
        matching_files = [f for f in all_files if f.endswith(suffix)]
        
        if not matching_files:
            continue  # Skip if no files match
        
        merged_df = pd.DataFrame()
        
        for file in matching_files:
            file_path = os.path.join(output_path, file)
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.replace(" ", "_")  # Replace spaces with underscores in column names
            if suffix == "_match.csv":
                merged_df["tournament"] = camp
            merged_df = pd.concat([merged_df, df], ignore_index=True)
        
        # Drop specified columns after merging
        drop_columns = suffixes_to_drop[suffix]
        merged_df.drop(columns=[col for col in drop_columns if col in merged_df.columns], inplace=True, errors='ignore')
        
        
        # Make replacements in the merged "_teams.csv" table
        if suffix == "_teams.csv":
            merged_df.rename(columns={"letter": "team"}, inplace=True)
            merged_df["team"] = merged_df["team"].replace({"A": "Team A", "B": "Team B"})
            
        
        if suffix == "_players_economy.csv":
            merged_df["player_side"] = merged_df["player_side"].replace({3: "Counter Terrorist", 2: "Terrorist"})
            
        if suffix == "_match.csv":
            merged_df["tournament"] = camp
            merged_df["date"] = pd.to_datetime(merged_df["date"])
            
        
        # Save the merged DataFrame
        if not os.path.exists(tabelas_finais):
            os.makedirs(tabelas_finais)
        output_file = os.path.join(tabelas_finais, f"{camp_var}{suffix}")
        merged_df.to_csv(output_file, index=False)

        
        
    print(f"All tables have been merged and saved to {tabelas_finais}.")
