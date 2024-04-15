import aiohttp
import asyncio
from zipfile import ZipFile
import os
from icecream import ic


async def download_zip_file(url, save_path, extract_dir):
    try:
        # Perform health check on the FQDN
        fqdn = url.split("/")[2]
        ic(f"Checking health of 'https://{fqdn}'...")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://{fqdn}", timeout=10) as response:
                if response.status == 403:
                    ic("Link is alive, but access is forbidden.")
                else:
                    response.raise_for_status()
                    ic("Link is alive!")

        # Download and save the ZIP file
        ic(f"Downloading ZIP file from '{url}'...")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                with open(save_path, "wb") as f:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
        ic(f"ZIP file downloaded successfully and saved as '{save_path}'!")

        # Extract the ZIP file
        ic(f"Extracting ZIP file to '{extract_dir}'...")
        with ZipFile(save_path, "r") as zipf:
            zipf.extractall(extract_dir)
        ic("Extraction complete!")
    except aiohttp.ClientResponseError as e:
        ic(f"Error: {e}")
    except IOError as e:
        ic(f"Error: {e}")
    except Exception as e:
        ic(f"Unexpected error: {e}")


async def main(url, save_path, extract_dir):
    try:
        await download_zip_file(url, save_path, extract_dir)
    except Exception as e:
        ic(f"An error occurred: {e}")


if __name__ == "__main__":
    url = "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/b3pn4kwpmn-3.zip"
    save_path = os.path.join(os.getcwd(), "file.zip")
    extract_dir = os.path.join(os.getcwd(), "data")

    # Create the "data" directory if it doesn't exist
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    asyncio.run(main(url, save_path, extract_dir))
