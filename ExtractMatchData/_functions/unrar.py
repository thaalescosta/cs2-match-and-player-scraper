import shutil
import os
import rarfile
from tqdm import tqdm  # Import tqdm for progress bar


def unrar(tournaments_df):
    '''
    Set the path to the unrar executable
    Download UnRAR from https://www.rarlab.com/rar/unrarw64.exe and extract it to a folder
    '''
    rarfile.UNRAR_TOOL = os.path.join(tournaments_df.iloc[0]['root'], r"_resources", "unrar.exe")  # Path for the unrar executable

    # Define the source folder containing .rar files
    source_folder = os.path.join(tournaments_df.iloc[0]['root'], "downloads", 'demos')
    
    # Get the list of .rar files
    rar_files = [f for f in os.listdir(source_folder) if f.endswith('.rar')]

    if not rar_files:
        print("No .rar files found for extraction.")
        return

    # Initialize tqdm progress bar
    progress_bar = tqdm(total=len(rar_files),
                        desc="Exctracting .rar   ", 
                        maxinterval=1.0,
                        unit="match",
                        ncols=100,  # Adjust the width of the progress bar
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
                        )

    # Add a new column 'demo_path' to the DataFrame
    tournaments_df['demo_path'] = None

    # Iterate over each .rar file and extract it
    for rar_filename in rar_files:
        # Find the corresponding 'tournament' value for the .rar file
        match = tournaments_df[tournaments_df['file_name'] == rar_filename]

        if match.empty:
            print(f"Skipping {rar_filename} (No matching tournament found).")
            progress_bar.update(1)
            continue
        
        tournament = match['tournament'].values[0]  # Get the tournament value
        destination_folder = os.path.join(tournaments_df.iloc[0]['root'], r"downloads", r'unpacked_demos', tournament)

        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        rar_path = os.path.join(source_folder, rar_filename)

        try:
            # Extract the .rar file
            with rarfile.RarFile(rar_path) as rf:
                rf.extractall(path=destination_folder)
        except rarfile.RarCannotExec as e:
            print(f"Error extracting {rar_filename}: {e}. Ensure 'unrar' is installed and accessible in your system's PATH.")
        except Exception as e:
            print(f"An error occurred with {rar_filename}: {e}")

        # Update the 'demo_path' column for the corresponding row
        tournaments_df.loc[tournaments_df['file_name'] == rar_filename, 'demo_path'] = destination_folder

        progress_bar.update(1)  # Update tqdm progress bar after each file

    progress_bar.close()  # Close tqdm progress bar

    # Remove the source folder after extraction
    # if os.path.exists(source_folder):
    #     shutil.rmtree(source_folder)
    
    return tournaments_df
