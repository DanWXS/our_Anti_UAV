import cv2
import numpy as np
import os

def pad_image(image, target_size):
    height, width = image.shape[:2]
    top = (target_size - height) // 2
    bottom = target_size - height - top
    left = (target_size - width) // 2
    right = target_size - width - left

    padded_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    return padded_image, top, left

def adjust_labels_for_padding(labels, top, left, target_width, target_height, original_width, original_height):
    adjusted_labels = []
    for label in labels:
        class_id, x_center, y_center, width, height = label
        y_center_new = (y_center * original_height + top) / target_height
        adjusted_labels.append([class_id, x_center, y_center_new, width, height])
    return adjusted_labels

def process_image_and_labels(image_path, labels, target_size, output_dir):
    image = cv2.imread(image_path)
    padded_image, top, left = pad_image(image, target_size)
    output_image_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(output_image_path, padded_image)

    original_width = image.shape[1]
    original_height = image.shape[0]
    target_width = target_size
    target_height = target_size

    adjusted_labels = adjust_labels_for_padding(labels, top, left, target_width, target_height, original_width, original_height)

    output_label_path = os.path.join(output_dir, os.path.basename(image_path).replace('.jpg', '.txt'))
    with open(output_label_path, 'w') as f:
        for label in adjusted_labels:
            f.write(f"{label[0]} {label[1]:.6f} {label[2]:.6f} {label[3]:.6f} {label[4]:.6f}\n")

def batch_process_images_and_labels(directory, target_size, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_name.endswith('.jpg'):
            image_path = file_path
            label_path = file_path.replace('.jpg', '.txt')

            if os.path.exists(label_path):
                labels = []
                with open(label_path, 'r') as f:
                    for line in f:
                        try:
                            labels.append(list(map(float, line.strip().split())))
                        except ValueError:
                            print(f"Skipping invalid label line in {label_path}: {line.strip()}")

                process_image_and_labels(image_path, labels, target_size, output_dir)

# Example usage
directory = r"D:\train\IR\train_data"
output_dir = r"D:\train\IR\train_data_padding"
target_size = 640

batch_process_images_and_labels(directory, target_size, output_dir)