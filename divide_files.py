import os
import shutil


base_path = r"D:\train\converted_labels"
train_data_path = "D:/train/train_data"
test_data_path = "D:/train/test_data"
eval_data_path = "D:/train/evaluate_data"

def my_filter(source):
    for name in os.listdir(source):
        if name.startswith('IR'):
            parts = name.split('-')
            if len(parts) == 2 and parts[0][2:].isdigit():
                num = int(parts[0][2:])
                if num<=80: # train_data
                    shutil.move(os.path.join(source,name),train_data_path)
                elif 80<num<=95: #test_data
                    shutil.move(os.path.join(source,name),test_data_path)
                else: #eval_data
                    shutil.move(os.path.join(source,name),eval_data_path)

my_filter(base_path)
