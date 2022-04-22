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
