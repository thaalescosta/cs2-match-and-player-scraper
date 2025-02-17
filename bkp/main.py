from ExtractMatchData._functions.get_matches_url import get_matches_url
from ExtractMatchData._functions.get_team_data import get_match_ids
from ExtractMatchData._functions.get_request import get_request
from ExtractMatchData._functions.download_files import download_files
from ExtractMatchData._functions.get_player_photos import unrar
from ExtractMatchData._functions.extrair_dados import run_csda_on_demos
from ExtractMatchData._ETL.merge_files import merge_csv_files
import os
from ExtractMatchData._functions.chromelib import pd
from IPython.display import display

# pd.set_option('display.max_columns', None)  # Show all columns
# pd.set_option('display.width', None)  # Disable line wrapping
# pd.set_option('display.max_colwidth', None)  # Show full column content

pd.reset_option('display.max_rows')
pd.reset_option('display.max_columns')
pd.reset_option('display.width')
pd.reset_option('display.max_colwidth')
# -------------------------------------------------------------------------
#   The ID of each event can be found in HLTV in either of the links below
#   For example: 
#   https://www.hltv.org/events/7909/blast-bounty-2025-season-1-finals
#   https://www.hltv.org/results?event=7909
# -------------------------------------------------------------------------

id_event = [7909,  # Blast Bounty 2025 Season 1 Finals
            7903 # Blast Bounty 2025 Season 1 
            # 7524, # Perfect World Shanghai Major 2024
            # 7557  # BLAST Premier World Final 2024
            ]

root = os.getcwd() # Get the root directory

# Gets the URLs from all the matches in the event and other info into a pandas dataframe
tournaments_df = get_matches_url(*id_event)

# Get an ID for each match used in a url
tournaments_df = get_match_ids(tournaments_df)

# Makes a get request to fetch the direct links to download the demos
tournaments_df = get_request(tournaments_df)
                           
# Makes the request to fetch the direct link to download the demos
tournaments_df = download_files(tournaments_df)

unrar(tournaments_df)

tournaments_df = run_csda_on_demos(tournaments_df)
match_data = merge_csv_files(tournaments_df)

# Access individual DataFrames
matches_df = match_data['_match']
teams_df = match_data['_teams']
kills_df = match_data['_kills']
players_df = match_data['_players']
players_economy_df = match_data['_players_economy']
clutches_df = match_data['_clutches']

# Display DataFrames
print("\nMatches:")
display(matches_df)

print("\nTeams:")
display(teams_df)

print("\nKills:")
display(kills_df)

print("\nPlayers:")
display(players_df)

print("\nPlayers Economy:")
display(players_economy_df)

print("\nClutches:")
display(clutches_df)


# Just exporting the tables in markdown format
output_dir = "github_tables"
os.makedirs(output_dir, exist_ok=True)
    
output_file = os.path.join(output_dir, "all_tables.txt")
with open(output_file, 'w') as f:
    for name, df in match_data.items():
        # Write table name as header
        f.write(f"\n{name.strip('_')} Table:\n")
        # Write header row
        f.write('| ' + ' | '.join(df.columns) + ' |\n')
        # Write separator row
        f.write('|' + '|'.join(['---' for _ in df.columns]) + '|\n')
        # Write first data row only
        first_row = df.iloc[0].astype(str)
        f.write('| ' + ' | '.join(first_row) + ' |\n')
        f.write('\n') # Add blank line between tables
    print(f"Saved all tables to {output_file}")
    
# Export tables to csv
for name, df in match_data.items():
    output_file = os.path.join(output_dir, f"{name.strip('_')}.csv")
    df.to_csv(output_file, index=False)
    print(f"Saved {output_file}")