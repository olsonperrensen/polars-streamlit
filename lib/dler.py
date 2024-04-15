import aiohttp
import asyncio
from zipfile import ZipFile, BadZipFile
import os
from typing import Optional
import concurrent.futures
from tqdm import tqdm
from icecream import ic


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


async def main(url: str, save_path: str, extract_dir: str):
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

    except Exception as e:
        ic(f"An error occurred: {e}")


if __name__ == "__main__":
    # url = "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/b3pn4kwpmn-3.zip"
    url = "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-large-zip-file.zip"
    save_path = "file.zip"
    extract_dir = os.path.join(os.getcwd(), "data")

    asyncio.run(main(url, save_path, extract_dir))
