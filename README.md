# Banned Words Checker for Federal Grants

An easy-to-use web application for researchers to analyze documents for the frequency of specific words and phrases. This tool was developed by the **SIM Lab** at **Southern Illinois University Edwardsville**.

## About The Project

This tool allows users to upload a document in `.docx` or `.pdf` format. It then processes the text to identify and count occurrences of words from a predefined "banned words" list. The results are displayed in a clean, sorted table showing each found phrase and its frequency.

The primary goal is to provide a simple, no-cost, browser-based utility for research and writing analysis.

### Built With

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [python-docx](https://python-docx.readthedocs.io/en/latest/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You must have Python 3.8 or newer installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Installation & Local Setup

1. **Clone the repository:**
    
    ```
    git clone https://github.com/SIM-Lab-SIUE/banned-word-checker.git
    cd banned-word-checker
    
    ```
    
2. **Create and activate a virtual environment (recommended):**
    - **Windows:**
        
        ```
        python -m venv .venv
        .\.venv\Scripts\activate
        
        ```
        
    - **macOS / Linux:**
        
        ```
        python3 -m venv .venv
        source .venv/bin/activate
        
        ```
        
3. **Install the required packages:**
    
    ```
    pip install -r requirements.txt
    
    ```
    
4. **Run the Streamlit application:**
    
    ```
    streamlit run app.py
    
    ```
    
    Your default web browser should open a new tab with the running application.
    

### Project Structure

The repository is structured as follows:

```
├── .streamlit/
│   └── config.toml      # Theming and color configuration
├── assets/
│   ├── simlab-atsiue.png  # Lab logo
│   └── siue-red-logo.png  # University logo
├── app.py                 # Main Streamlit application script
├── requirements.txt       # Python package dependencies
└── README.md              # This file

```

## Deployment

This application is designed to be easily deployed for free using [Streamlit Community Cloud](https://share.streamlit.io/).

1. Push your project to a public GitHub repository. Ensure all files, including the `.streamlit` and `assets` folders, are committed.
2. Sign up for Streamlit Community Cloud using your GitHub account.
3. Click "**New app**" and select the repository you just created.
4. Ensure the "Main file path" is set to `app.py`.
5. Click "**Deploy!**"

Streamlit will handle the rest, and your application will be live on a public URL.

## Customization

### Modifying the Banned Words List

The list of banned words and phrases is stored as a Python `set` named `BANNED_WORDS` at the top of the `app.py` file. You can directly edit this set to add or remove terms.

### Changing the Theme and Appearance

- **Colors:** The application's color scheme is defined in `.streamlit/config.toml`. You can change the hex codes in this file to match a different branding.
- **Fonts & Styles:** Custom fonts and other style overrides are handled using CSS injected via a `st.markdown()` call at the top of `app.py`. You can modify this CSS block to change the typography or other visual elements.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

The SIM Lab @ SIUE - [Lab Website](https://sim-lab-siue.github.io)

Project Link: `https://github.com/SIM-Lab-SIUE/banned-word-checker`