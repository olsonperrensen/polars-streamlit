import pandas as pd
import os
import threading
from icecream import ic, install
import logging

# Set up logging to a file
logging.basicConfig(
    filename="conversion_log.txt",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
install()


def delete_csv_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                ic(f"Deleting file: '{file_path}'")
                logging.info(f"Deleting file: '{file_path}'")
                os.remove(file_path)


def convert_to_parquet():
    # Set input and output folders to the "data/" subdirectory
    input_folder = os.path.join(os.getcwd(), "data")
    output_dir = os.path.join(os.getcwd(), "data")

    # Recursive function to find and convert CSV files
    def convert_csv_to_parquet(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".csv"):
                    input_file = os.path.join(root, file)
                    relative_path = os.path.relpath(root, input_folder)
                    output_file = os.path.join(
                        output_dir,
                        relative_path,
                        f"{os.path.splitext(file)[0]}.parquet",
                    )
                    os.makedirs(os.path.join(output_dir, relative_path), exist_ok=True)

                    ic(f"Converting '{input_file}' to '{output_file}'")
                    logging.info(f"Converting '{input_file}' to '{output_file}'")

                    # Read CSV file and save as Parquet
                    df = pd.read_csv(input_file)
                    df.to_parquet(output_file)

                    ic(f"Conversion successful: '{output_file}'")
                    logging.info(f"Conversion successful: '{output_file}'")

    # Convert all CSV files in the input folder and its subdirectories
    threads = []
    for root, dirs, files in os.walk(input_folder):
        for dir in dirs:
            t = threading.Thread(
                target=convert_csv_to_parquet, args=(os.path.join(root, dir),)
            )
            t.start()
            threads.append(t)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    ic("All conversions completed successfully.")
    logging.info("All conversions completed successfully.")

    # Delete all CSV files in the input folder and its subdirectories
    delete_csv_files(input_folder)


if __name__ == "__main__":
    convert_to_parquet()
