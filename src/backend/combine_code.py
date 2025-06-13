import os
#本文用来读取代码
output_file = "all_code.txt"  # 输出文件名
skip_dirs = ["venv", "__pycache__"]  # 跳过目录
extensions = [".py"]  # 要合并的扩展名

with open(output_file, "w", encoding="utf-8") as outfile:
    for root, dirs, files in os.walk(os.getcwd()):
        # 跳过指定目录
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                # 添加文件名作为分隔标记
                outfile.write(f"\n\n{'=' * 50}\n# File: {file_path}\n{'=' * 50}\n\n")
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())