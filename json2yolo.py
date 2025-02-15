import json
import os

def convert_annotations(json_path, output_dir, file_index):
    # 读取JSON文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 获取图像宽度和高度
    image_width = 640  # 假设图像宽度为640
    image_height = 512  # 假设图像高度为512

    # 类别映射
    class_mapping = {
        "exist_uav": 0
    }

    # 转换标签
    line_index = 1
    for idx, exist in enumerate(data['exist']):
        output_path = os.path.join(output_dir, f"IR{file_index}-{line_index}.txt")
        if exist == 1:
            bbox = data['gt_rect'][idx]
            x_min, y_min, width, height = bbox

            # 计算中心点坐标和宽高
            x_center = (x_min + width / 2) / image_width
            y_center = (y_min + height / 2) / image_height
            width /= image_width
            height /= image_height

            yolo_label = f"{class_mapping['exist_uav']} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(yolo_label + '\n')
        else:
            # 生成空文件
            open(output_path, 'w', encoding='utf-8').close()
        line_index += 1

def process_ir_labels(base_path, output_base_path):
    # 检查并创建输出目录
    if not os.path.exists(output_base_path):
        os.makedirs(output_base_path)

    file_index = 1
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if 'IR_label' in file and file.endswith('.json'):
                json_path = os.path.join(root, file)
                convert_annotations(json_path, output_base_path, file_index)
                file_index += 1

base_path = r'C:\Users\28585\Desktop\DC\UAV-300\dataset\test-dev'
output_base_path = r'C:\Users\28585\Desktop\DC\UAV-300\dataset\converted_labels'

process_ir_labels(base_path, output_base_path)