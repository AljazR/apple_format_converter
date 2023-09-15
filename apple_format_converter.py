# The script converts all HEIC files in a directory to JPG and MOV files to MP4.
# All converted files are saved in a new directory, including other files that are not converted.

# Usage:
# 1. Change directory and new_directory variables to the desired paths
# 2. Run the script with: python3 heic_converter.py

# Requirements:
# Pillow: pip install Pillow
# pillow-heif: pip install pillow-heif
# ffmpeg: sudo apt-get install ffmpeg

import os
import subprocess
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

# directory = '<<PATH>>'
directory = '/mnt/c/Users/aljoz/Desktop/FRI/projects/convert_from_heic/test'

# new_directory = '<<NEW PATH>>'
new_directory = '/mnt/c/Users/aljoz/Desktop/FRI/projects/convert_from_heic/test - converted'

# Create new directory if it doesn't exist and exit if it does - it can be dangerous to overwrite files
if not os.path.exists(new_directory):
    os.makedirs(new_directory)
else:
    print(f'Directory "{new_directory.split("/")[-1]}" already exists. Please choose a different name. It can be dangerous to overwrite files.')
    exit()

# Rename files that would have the same name after conversion and would be overwritten
for filename in os.listdir(directory):
    if filename.endswith(".HEIC") or filename.endswith(".heic"):
        if os.path.exists(os.path.join(directory, os.path.splitext(filename)[0] + '.jpg')):
            os.rename(os.path.join(directory, filename), os.path.join(directory, os.path.splitext(filename)[0] + ' (' + os.path.splitext(filename)[1] + ')' + os.path.splitext(filename)[1]))
    elif filename.endswith(".MOV") or filename.endswith(".mov"):
        if os.path.exists(os.path.join(directory, os.path.splitext(filename)[0] + '.mp4')):
            os.rename(os.path.join(directory, filename), os.path.join(directory, os.path.splitext(filename)[0] + ' (' + os.path.splitext(filename)[1] + ')' + os.path.splitext(filename)[1]))
    
# Get number of files in directory
num_files = len([f for f in os.listdir(directory)if os.path.isfile(os.path.join(directory, f))])

for i, filename in enumerate(os.listdir(directory), 1):
    # Print current status
    print('\033[F', end='')
    print(f'Processing file {i}/{num_files}: {filename}')

    # Convert image file
    if filename.endswith(".HEIC") or filename.endswith(".heic"):
        image = Image.open(os.path.join(directory, filename))
        image.convert('RGB').save(os.path.join(new_directory, os.path.splitext(filename)[0] + '.jpg'))
    
    # Convert video file
    elif filename.endswith(".MOV") or filename.endswith(".mov"):
        subprocess.call(['ffmpeg', '-i', os.path.join(directory, filename), os.path.join(new_directory, os.path.splitext(filename)[0] + '.mp4')], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
   
    # Copy other files
    else:
        subprocess.call(['cp', os.path.join(directory, filename), os.path.join(new_directory, filename)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)