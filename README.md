# youtube

This program retrieves data from the YouTube JSON API v3, stores the data in a sqlite database, displays the data (view_count, like_count, comment_count) in individual matplotlib charts using the date on the x axis.Then it stores the retrieved data in a csv in the data directory, allowing the user to analyze the data in a way he/she
sees fit. 

---

## Up and Running

To run the code as intended, you need to add PYTHONPATH to .bashrc. Run this command: `nano ~/.bashrc`

Then you need to add the PYTHONPATH to the bashrc file: `export PYTHONPATH="."`, then exit.

To run the code, run `source ~/.bashrc`

Get into the project root to create the virtual environment and install the dependencies:

    python -m venv .venv

    source .venv/bin/activate

    pip install -r requirements.txt


## Environment Variables

The program expect that a valid API key to access the JSON API. To store and use the API key, the program uses a package called `python-dotenv` to store this key for program use. The file the key is stored in a file called `.env` in the project root, and the program expects it to be like this:

    YOUTUBE_API_KEY=<YOUTUBE_API_KEY>

Instructions on obtaining a YouTube API key can be obtained [HERE](https://developers.google.com/youtube/v3/getting-started "YouTube Data API Overview").


## Running The Program

`python youtube <handle>`

Handle is the handle of the YouTube channel that you want data on. The handle argument need not have the `@` symbol; it will be added automatically.
