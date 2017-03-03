# pus-homework-verificator
Get list of uploaded homeworks from ELF3 and put summary into Google Sheet

## Configure

1. Install dependency modules:
 
`pip install --upgrade google-api-python-client responses`

2. Setup ELF3 credentials:

Do `cp src/credentials.py.sample src/credentials.py` and setup your login and
password to ELF3. 

3. Setup access to Google Sheet API:

Go to [Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)
site and get `client_secret.json` and save as `src/client_secret.json`.

4. Run `src/main.py` in your desktop.
5. When your default browser is open confirm access to Google API.
Confirmation will be stored in `~/.google_api_credentials`.
6. Copy `src/` and `~/.google_api_credentials` to your server and configure CRON.
