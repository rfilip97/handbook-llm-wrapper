import subprocess
import os
import shutil

from config import REPO_URL, TMP_HANDBOOK_PATH, TMP_DATA_SOURCE_PATH


def run():
    if os.path.exists(TMP_HANDBOOK_PATH):
        return

    clone_repository()
    copy_md_files()


def clone_repository():
    try:
        subprocess.run(["git", "clone", REPO_URL, TMP_HANDBOOK_PATH], check=True)

        print(f"Repository cloned to {os.path.abspath(TMP_HANDBOOK_PATH)}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def copy_md_files():
    if not os.path.exists(TMP_DATA_SOURCE_PATH):
        os.makedirs(TMP_DATA_SOURCE_PATH)

    for root, dirs, files in os.walk(TMP_HANDBOOK_PATH):
        for file in files:
            if file.endswith(".md") and not file.startswith("_"):
                parts = root.split(os.sep)

                if len(parts) > 1 and parts[-1].startswith("_"):
                    source_file = os.path.join(root, file)
                    target_file = os.path.join(TMP_DATA_SOURCE_PATH, file)
                    shutil.copy2(source_file, target_file)
                    print(f"Copied {source_file} to {target_file}")
