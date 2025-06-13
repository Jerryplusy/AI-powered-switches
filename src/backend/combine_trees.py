import os
#本文件用来生成项目树
def generate_directory_tree(startpath, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write(f"{indent}{os.path.basename(root)}/\n")
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write(f"{subindent}{file}\n")

# 使用当前项目目录
project_path = os.getcwd()
output_file = 'project_structure.txt'
generate_directory_tree(project_path, output_file)
print(f"目录结构已生成到 {output_file}")