import tkinter as tk
from tkinter import filedialog
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


def convert_to_parquet():
    # Open file dialog to select input folder
    input_folder = filedialog.askdirectory(title="Select input folder")

    if input_folder:
        # Create a directory to store the Parquet files
        output_dir = filedialog.askdirectory(title="Select output directory")

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
                        os.makedirs(
                            os.path.join(output_dir, relative_path), exist_ok=True
                        )

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

        # Display success message
        result_label.config(
            text="Conversion successful!", fg="#1DB954", font=("Helvetica", 16, "bold")
        )


# Create the main window
root = tk.Tk()
root.title("CSV to Parquet Converter")
root.geometry("500x300")
root.configure(bg="#121212", padx=20, pady=20)

# Create the convert button
convert_button = tk.Button(
    root,
    text="Convert CSV to Parquet",
    command=convert_to_parquet,
    bg="#1DB954",
    fg="#FFFFFF",
    font=("Helvetica", 14, "bold"),
    relief="flat",
    activebackground="#1ED760",
)
convert_button.pack(pady=20)

# Create the result label
result_label = tk.Label(
    root, text="", fg="#FFFFFF", bg="#121212", font=("Helvetica", 14)
)
result_label.pack(pady=10)

# Run the main loop
root.mainloop()
