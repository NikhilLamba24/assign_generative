import os

def find_images_in_directory(directory):
    # List of image extensions to be checked extensively
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    # List to store the full paths of images
    image_paths = []
    
    # Going through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # checking for image extension inside teh file
            if any(file.lower().endswith(ext) for ext in image_extensions):
                # complete path of image
                image_paths.append(os.path.join(root, file))
    
    return image_paths


