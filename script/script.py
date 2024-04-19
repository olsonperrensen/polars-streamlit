import logging
import pandas as pd
import threading
import aiohttp
import asyncio
from zipfile import ZipFile, BadZipFile
import os
from typing import Optional
import concurrent.futures
from tqdm import tqdm
from icecream import ic
import tempfile


async def download_chunk(session, url, start, end, chunk_size, file_path, progress_bar):
    headers = {"Range": f"bytes={start}-{end}"}
    async with session.get(url, headers=headers) as response:
        with open(file_path, "rb+") as f:
            f.seek(start)
            while True:
                chunk = await response.content.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                progress_bar.update(len(chunk))


async def download_zip_file(
    url: str, save_path: str, extract_dir: str, num_connections: int = 8
) -> Optional[str]:
    try:
        ic(
            f"Checking if any ZIP file already exists in '{os.path.dirname(save_path)}'..."
        )
        existing_zip_files = [
            f for f in os.listdir(os.path.dirname(save_path)) if f.endswith(".zip")
        ]
        if existing_zip_files:
            ic(f"Found existing ZIP file(s): {', '.join(existing_zip_files)}")
            save_path = os.path.join(os.path.dirname(save_path), existing_zip_files[0])
            ic(f"Using existing ZIP file: '{save_path}'")
        else:
            ic(f"No existing ZIP file found. Downloading from '{url}'...")
            async with aiohttp.ClientSession() as session:
                async with session.head(url) as response:
                    total_size = int(response.headers["Content-Length"])

                chunk_size = total_size // num_connections
                remaining_size = total_size % num_connections

                with open(save_path, "wb") as f:
                    f.write(b"\0" * total_size)

                with tqdm(
                    total=total_size, unit="B", unit_scale=True, desc="Downloading"
                ) as progress_bar:
                    tasks = []
                    for i in range(num_connections):
                        start = i * chunk_size
                        end = start + chunk_size - 1
                        if i == num_connections - 1:
                            end += remaining_size
                        task = asyncio.ensure_future(
                            download_chunk(
                                session,
                                url,
                                start,
                                end,
                                chunk_size,
                                save_path,
                                progress_bar,
                            )
                        )
                        tasks.append(task)

                    await asyncio.gather(*tasks)

            ic(f"ZIP file downloaded successfully and saved as '{save_path}'!")

            if not save_path.endswith("A.zip"):
                ic(f"Renaming '{save_path}' to 'A.zip'...")
                new_save_path = os.path.join(os.path.dirname(save_path), "A.zip")
                os.rename(save_path, new_save_path)
                save_path = new_save_path
                ic(f"ZIP file renamed to '{save_path}'")

        ic("Checking the integrity of the downloaded ZIP file...")
        try:
            with ZipFile(save_path, "r") as zipf:
                if zipf.testzip() is not None:
                    return "Error: The downloaded ZIP file is corrupted."
            ic("ZIP file integrity check passed!")
        except BadZipFile:
            return "Error: The downloaded ZIP file is corrupted."

        ic("Checking the contents of the ZIP file...")
        with ZipFile(save_path, "r") as zipf:
            namelist = zipf.namelist()
            ic(f"Contents of the ZIP file: {namelist}")

            if namelist:
                ic("Renaming folders inside the ZIP file...")
                # Get the name of the root folder
                root_folder = namelist[0].split("/")[0]
                ic(f"Root folder: {root_folder}")

                # Create a temporary directory to store the modified ZIP contents
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Extract the ZIP contents to the temporary directory
                    zipf.extractall(temp_dir)

                    # Rename the root folder to "A"
                    old_root_path = os.path.join(temp_dir, root_folder)
                    new_root_path = os.path.join(temp_dir, "A")
                    os.rename(old_root_path, new_root_path)
                    ic("Root folder renamed to 'A'")

                    # # Rename the subfolder from "GAMEEMO" to "B"
                    # old_subfolder_path = os.path.join(new_root_path, "GAMEEMO")
                    # new_subfolder_path = os.path.join(new_root_path, "B")
                    # os.rename(old_subfolder_path, new_subfolder_path)
                    # ic("Subfolder renamed from 'GAMEEMO' to 'B'")

                    # Delete all .mat files inside the temporary directory
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            if file.endswith(".mat"):
                                os.remove(os.path.join(root, file))
                    ic("All .mat files deleted from the ZIP")

                    # Create a new ZIP file with the modified contents
                    with ZipFile(save_path, "w") as new_zipf:
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                new_zipf.write(
                                    file_path, os.path.relpath(file_path, temp_dir)
                                )
                    ic("Modified ZIP file written")
            else:
                ic("ZIP file is empty. Skipping renaming process.")

        ic(f"Extracting ZIP file to '{extract_dir}'...")
        with ZipFile(save_path, "r") as zipf:
            zipf.extractall(extract_dir)
        ic("Extraction complete!")

    except aiohttp.ClientResponseError as e:
        return f"Error: {e}"
    except IOError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

    return None


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


async def dl_script(url: str, save_path: str, extract_dir: str):
    try:
        # Check if the ZIP file is already downloaded in the "data/" subdirectory
        data_dir = os.path.join(os.getcwd(), "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        data_save_path = os.path.join(data_dir, os.path.basename(save_path))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                asyncio.run, download_zip_file(url, data_save_path, extract_dir)
            )
            error_message = future.result()

        if error_message:
            ic(error_message)
            return

        # Convert CSV files to Parquet format
        convert_to_parquet()

    except Exception as e:
        ic(f"An error occurred: {e}")


if __name__ == "__main__":
    # url = "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/b3pn4kwpmn-3.zip"
    url = "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-large-zip-file.zip"
    save_path = "file.zip"
    extract_dir = os.path.join(os.getcwd(), "data")

    asyncio.run(dl_script(url, save_path, extract_dir))
