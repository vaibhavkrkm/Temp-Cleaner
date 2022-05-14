import os
import shutil

def delete_dir_contents(folder_path):
    try:
        for content in os.listdir(folder_path):
            content_path = os.path.join(folder_path, content)

            if (os.path.isfile(content_path)):
                try:
                    os.unlink(content_path)
                except:
                    pass
            elif (os.path.isdir(content_path)):
                try:
                    shutil.rmtree(content_path)
                except:
                    pass
        return None
    except Exception as e:
        return e


def get_readable_size(raw_size):
    """
    Converts size (bytes) into readable size
    """
    # step 1: convert into kb
    readable_size = raw_size / 1024
    unit = "KB"

    # step 2: convert into mb if necessary
    if (readable_size > 1024):
        readable_size /= 1024
        unit = "MB"

        if (readable_size > 1024):
            readable_size /= 1024
            unit = "GB"
    
    readable_size = round(readable_size, 1)
    return f"{readable_size} {unit}"
