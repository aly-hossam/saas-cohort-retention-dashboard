import os
import zipfile
import tarfile

def extract_all_archives(source_dir=None, output_folder_name="extracted_files", ignore_macosx=True):
    """
    Finds and extracts all zip/tar archive files in the specified directory.
    Ignores __MACOSX metadata files by default.
    """
    # Determine the directory where the script is running
    if source_dir is None:
        if '__file__' in globals():
            source_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            source_dir = os.getcwd()

    # Destination directory for extracted content
    destination_dir = os.path.join(source_dir, output_folder_name)
    os.makedirs(destination_dir, exist_ok=True)

    print(f"Scanning directory: {source_dir}")
    print(f"Extracting contents to: {destination_dir}\n")

    for root, dirs, files in os.walk(source_dir):
        # Prevent scanning inside the output destination folder
        if destination_dir in root:
            continue

        for file in files:
            file_path = os.path.join(root, file)

            # 1. Handle ZIP files
            if file.lower().endswith('.zip'):
                print(f"[*] Found ZIP archive: {file}")
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        for member in zip_ref.infolist():
                            # Skip macOS hidden metadata files if enabled
                            if ignore_macosx and member.filename.startswith('__MACOSX/'):
                                continue
                            zip_ref.extract(member, destination_dir)
                    print(f"    [+] Successfully extracted: {file}")
                except Exception as e:
                    print(f"    [-] Error extracting {file}: {e}")

            # 2. Handle TAR files (.tar, .tar.gz, .tgz, etc.)
            elif file.lower().endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2')):
                print(f"[*] Found TAR archive: {file}")
                try:
                    with tarfile.open(file_path, 'r') as tar_ref:
                        for member in tar_ref.getmembers():
                            if ignore_macosx and member.name.startswith('__MACOSX/'):
                                continue
                            tar_ref.extract(member, destination_dir)
                    print(f"    [+] Successfully extracted: {file}")
                except Exception as e:
                    print(f"    [-] Error extracting {file}: {e}")

    print("\n[✔] Extraction process completed successfully.")

if __name__ == "__main__":
    extract_all_archives()