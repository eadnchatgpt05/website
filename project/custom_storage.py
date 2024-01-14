# custom_storage.py
from django.core.files.storage import FileSystemStorage
import os 


class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Get the directory path and file extension
        directory, filename = os.path.split(name)
        root, ext = os.path.splitext(filename)

        # Iterate to find a unique filename with incremental numbers
        i = 1
        while self.exists(name):
            # Format the filename with leading zeros
            incremented_name = f"{root}_{i:04d}{ext}"
            name = os.path.join(directory, incremented_name)
            i += 1

        return name