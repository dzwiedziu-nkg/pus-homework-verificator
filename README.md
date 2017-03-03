# pus-homework-verificator
Get list of uploaded homeworks from ELF3 and put summary into Google Sheet

## Configure

### Install dependency modules
 
`pip install --upgrade google-api-python-client responses`

### Setup ELF3 credentials

Do `cp src/credentials.py.sample src/credentials.py` and setup your login and
password to ELF3. 

### Setup access to Google Sheet API:

Go to [Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)
site and get `client_secret.json` and save as `src/client_secret.json`.

### Deploy to your server

1. Run `src/main.py` in your desktop.
2. When your default browser is open confirm access to Google API.
Confirmation will be stored in `~/.google_api_credentials`.
3. Copy `src/` and `~/.google_api_credentials` to your server.
4. Configure CRON to run `src/main.py` or run `run_per_hour.sh` bash script in `screen`.
