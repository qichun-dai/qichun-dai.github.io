import json
import os
from datetime import datetime, timedelta
from PIL import Image

def convert_heic_to_jpeg(heic_path, jpeg_path):
    os.system(f"heif-convert {heic_path} {jpeg_path}")

def get_image_metadata(folder_path):
    metadata = []
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith('.heic'):
                file_path = os.path.join(root, file_name)
                
                # Convert HEIC to JPEG
                base_name = os.path.splitext(file_name)[0]
                jpeg_file_name = base_name + '.jpeg'
                jpeg_file_path = os.path.join(root, jpeg_file_name)
                convert_heic_to_jpeg(file_path, jpeg_file_path)
                
                # Read the JPEG file and get its dimensions
                with Image.open(jpeg_file_path) as img:
                    width, height = img.size
                    orientation = 'vertical' if height > width else 'horizontal'
                
                creation_time = os.path.getmtime(file_path)
                creation_time = datetime.fromtimestamp(creation_time) - timedelta(hours=2)
                creation_time = creation_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                
                metadata.append({
                    'fileName': jpeg_file_name,
                    'creationTime': creation_time,
                    'orientation': orientation,
                    'width': width,
                    'height': height
                })
    metadata = sorted(metadata, key=lambda x: x['creationTime'])
    return metadata

def save_metadata_to_json(metadata, output_file_path):
    with open(output_file_path, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

# Specify the folder containing the image files
folder_path = '/Users/qichun/Documents/GitHub/camino/img/updates'
metadata = get_image_metadata(folder_path)

# Specify the output JSON file path
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file_path = os.path.join(script_dir, 'metadata.json')
save_metadata_to_json(metadata, output_file_path)