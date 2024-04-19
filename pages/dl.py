import streamlit as st
import requests


def main():
    st.title("Dataset Processing")

    # Define the available dataset URLs
    dataset_urls = {
        "Sample Large ZIP File": "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-large-zip-file.zip",
        "Medical Dataset": "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/b3pn4kwpmn-3.zip",
        # Add more dataset options as needed
    }

    # Create a dropdown to select the dataset URL
    selected_url = st.selectbox("Select a dataset:", list(dataset_urls.keys()))

    if st.button("Process Dataset"):
        # Get the selected dataset URL
        url = dataset_urls[selected_url]
        save_path = "file.zip"
        extract_dir = "data"

        # Send a request to the FastAPI endpoint to start the dataset processing
        response = requests.post(
            "http://localhost:8000/process_dataset",
            json={"url": url, "save_path": save_path, "extract_dir": extract_dir},
        )

        if response.status_code == 200:
            st.success("Dataset processing started in the background.")
        else:
            st.error("Failed to start dataset processing.")


if __name__ == "__main__":
    main()
