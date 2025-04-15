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
    
    # Get unique file names from the DataFrame
    unique_files = tournaments_df['file_name'].unique()

    if not unique_files.any():
        print("No files found for extraction.")
        return tournaments_df

    # Initialize tqdm progress bar
    progress_bar = tqdm(total=len(unique_files),
                        desc="Extracting .rar   ", 
                        maxinterval=1.0,
                        unit="match",
                        ncols=100,  # Adjust the width of the progress bar
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
                        )

    # # Add a new column 'demo_path' to the DataFrame if it doesn't exist
    # if 'demo_path' not in tournaments_df.columns:
    #     tournaments_df['demo_path'] = None

    # Iterate over each unique .rar file
    for rar_filename in unique_files:
        # Find the first matching tournament value for the .rar file
        match = tournaments_df[tournaments_df['file_name'] == rar_filename].iloc[0]
        
        tournament = match['tournament']  # Get the tournament value
        destination_folder = os.path.join(tournaments_df.iloc[0]['root'], r"downloads", r'unpacked_demos', tournament)

        # Create the destination folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        rar_path = os.path.join(source_folder, rar_filename)

        try:
            # Extract the .rar file
            with rarfile.RarFile(rar_path) as rf:
                rf.extractall(path=destination_folder)
                # Update the 'demo_path' column for all rows with this file_name immediately after successful extraction
                tournaments_df.loc[tournaments_df['file_name'] == rar_filename, 'demo_path'] = destination_folder
        except rarfile.RarCannotExec as e:
            print(f"Error extracting {rar_filename}: {e}. Ensure 'unrar' is installed and accessible in your system's PATH.")
        except Exception as e:
            print(f"An error occurred with {rar_filename}: {e}")

        progress_bar.update(1)  # Update tqdm progress bar after each file

    progress_bar.close()  # Close tqdm progress bar
    
    return tournaments_df
