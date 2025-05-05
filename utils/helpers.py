import os

def clean_old_reports(prefix: str, directory: str = "assets"):
    """
    Delete all files in the given directory that match the given prefix.
    """
    if not os.path.exists(directory):
        return

    for filename in os.listdir(directory):
        if prefix in filename and filename.endswith(".html"):
            os.remove(os.path.join(directory, filename))
