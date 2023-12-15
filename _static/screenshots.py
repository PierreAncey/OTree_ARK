import cv2
import os

# Define the root directory as the current directory
root_dir = '.'

# Iterate over each subfolder in the root directory
for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)

    # Check if the name of the folder is an integer, or skip the current loop iteration
    try:
        int(folder)
    except ValueError:
        continue

    # Check if it's a directory
    if os.path.isdir(folder_path):
        # Create a new folder for images
        images_folder = os.path.join(folder_path, 'images')
        os.makedirs(images_folder, exist_ok=True)

        # Iterate over each video in the folder
        for i in range(6):
            video_path = os.path.join(folder_path, f'{i}.mp4')

            # Check if the video file exists
            if os.path.isfile(video_path):
                # Read the video
                cap = cv2.VideoCapture(video_path)

                # Check if the video was opened successfully
                if cap.isOpened():
                    # Read the first frame
                    ret, frame = cap.read()

                    if ret:
                        # Save the first frame as a JPEG image
                        image_path = os.path.join(images_folder, f'{i}.jpg')
                        cv2.imwrite(image_path, frame)

                # Release the video capture object
                cap.release()

print("Processing complete.")