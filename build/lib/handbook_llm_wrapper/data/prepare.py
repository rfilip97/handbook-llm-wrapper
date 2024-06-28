import subprocess
import os
import shutil
from handbook_llm_wrapper.config import REPO_URL, TMP_HANDBOOK_PATH, TMP_DATA_SOURCE_PATH


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

    for root_path, _, files in os.walk(TMP_HANDBOOK_PATH):
        for filename in files:
            if is_valid_folder(root_path) and is_valid_file(filename):
                copy_file(filename, root_path, TMP_DATA_SOURCE_PATH)


def is_valid_file(file):
    return file.endswith(".md") and not file.startswith("_")


def is_valid_folder(root_path):
    parts = root_path.split(os.sep)

    return len(parts) > 1 and parts[-1].startswith("_")


def copy_file(filename, containing_folder, target_folder):
    source_file = os.path.join(containing_folder, filename)
    target_file = os.path.join(target_folder, filename)

    shutil.copy2(source_file, target_file)

    print(f"Copied {source_file} to {target_file}")
