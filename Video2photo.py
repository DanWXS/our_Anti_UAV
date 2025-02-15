import cv2
import os
import json

def video2photo(num, cat, video_path, output_path, exist_labels):
    os.makedirs(output_path, exist_ok=True)  # Create target directory

    vc = cv2.VideoCapture(video_path)  # Read video file
    if not vc.isOpened():  # Check if opened successfully
        return

    frames = []
    for i in range(len(exist_labels)):
        rval, frame = vc.read()
        if not rval or frame is None or frame.size == 0:
            break
        frames.append((frame, i + 1))

    vc.release()  # Release video capture object
    cv2.destroyAllWindows()  # Close all OpenCV windows

    for frame, idx in frames:
        cv2.imwrite(os.path.join(output_path, f'{cat}{num}-{idx}.jpg'), frame)  # Save frames as images

def is_video_file(file_path):
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv'}  # Use set for faster lookup
    return os.path.splitext(file_path)[1].lower() in video_extensions

def process_videos(base_path, rgb_base_path, ir_base_path):
    i = 0
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_video_file(file_path):
                file_name, _ = os.path.splitext(file)
                label_path = os.path.join(root, f'{file_name}_label.json')
                if os.path.exists(label_path):
                    with open(label_path, 'r', encoding='utf-8') as f:
                        labels = json.load(f)
                    exist_labels = labels.get('exist', [])
                    if 'RGB' in file_name:
                        video2photo(i, 'RGB', file_path, rgb_base_path, exist_labels)
                    elif 'IR' in file_name:
                        video2photo(i, 'IR', file_path, ir_base_path, exist_labels)
        i += 1

base_path = r"C:\Users\28585\Desktop\DC\UAV-300\dataset\test-dev"
rgb_base_path = r'D:\train\RGB'
ir_base_path = r"D:\train\converted_labels"

process_videos(base_path, rgb_base_path, ir_base_path)