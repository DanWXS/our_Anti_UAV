import os
import shutil

def delete_txt_files(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt'):
            file_path = os.path.join(directory, file_name)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

# Example usage
# directory = "D:/train/IR_RAW"
# delete_txt_files(directory)


def list_video_files(directory):
    video_extensions = ['.jpg']
    video_files = [f[0:4] for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in video_extensions]
    return video_files

# 示例用法
# directory = r"D:\train\IR\train_data"
# video_files = list_video_files(directory)
# print(list(set(video_files)))



def process_yolo_labels(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_name.endswith('.txt'):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            if not lines:
                continue  # Skip empty files

            with open(file_path, 'w') as file:
                for line in lines:
                    file.write(line.replace('0.0', '0'))


# Example usage
directory = r"D:\train\IR_padding\train_data_padding"
process_yolo_labels(directory)

