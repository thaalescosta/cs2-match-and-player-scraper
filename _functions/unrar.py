import os
import rarfile
from tqdm import tqdm  # Import tqdm for progress bar

def unrar(camp):
    # Explicitly set the path to the unrar executable (if needed)
    rarfile.UNRAR_TOOL = "C:/unrar-ia64/unrar.exe"  # For Windows

    # Define the source folder containing .rar files and the destination folder
    source_folder = f'./Downloads/{camp}'
    destination_folder = f'./Demos/{camp}'

    # Create the "Demos" folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get the list of .rar files
    rar_files = [f for f in os.listdir(source_folder) if f.endswith('.rar')]

    # Iterate over all .rar files with a progress bar
    for filename in tqdm(rar_files, desc="Demo unpacking", unit="file"):
        # Construct the full file path
        rar_path = os.path.join(source_folder, filename)
        
        try:
            # Open the .rar file
            with rarfile.RarFile(rar_path) as rf:
                # Extract all contents to the destination folder
                rf.extractall(path=destination_folder)
                # print(f"Extracted {filename} to {destination_folder}")
        except rarfile.RarCannotExec as e:
            print(f"Error extracting {filename}: {e}")
            print("Ensure 'unrar' is installed and accessible in your system's PATH.")
        except Exception as e:
            print(f"An error occurred with {filename}: {e}")
