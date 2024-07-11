import os
import shutil

def static_to_public(file_path_static, file_path_public):
    source_abs = os.path.abspath(file_path_static)
    destination_abs = os.path.abspath(file_path_public)

    if os.path.exists(destination_abs):
        shutil.rmtree(destination_abs)
    os.mkdir(destination_abs)
    
    # Determine the path for the log file, up one directory level
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log.txt")


    with open(log_file, "w") as file:
        file.truncate()

    def recursive_copy(src, dest):
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dest_item = os.path.join(dest, item)
            
            if os.path.isdir(src_item):
                os.mkdir(dest_item)
                recursive_copy(src_item, dest_item)
            else:
                shutil.copy(src_item, dest_item)
                with open(log_file, "a") as file:
                    file.write(f"Copied: {src_item} to {dest_item}\n")

    recursive_copy(source_abs, destination_abs)

