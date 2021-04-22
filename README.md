# qsheets.py
Questrade to Google Sheets bridge

## Introduction

qsheets is a simple python script that allows to retrieve stock market data from Questrade through it's REST API and populate one or multipe Google Sheets documents automatically.

## Pre-requistites

 \>= python 3

## Installation

### Python packages
The following packages also need to be installed:
```python
pip3 install gspread
pip3 install oauth2client
pip3 install questrade-api
pip3 install argparse
pip3 install pandas
```
### qsheets
Currently there is no installer script available (see [TODO list](#todo)). Please download the zip file from the Code menu on the top right of this [reposistory](https://github.com/boffyflow/qsheets).

Unzip the file downloaded to a convenient location on your system. For the sake of  documentation it is assumed that the files are unzipped to a folder: ```C:\user\johndoe\documents\qsheets```, but the files can be unzipped anywhere as long as the files stay together.

### Questrade Account Authentication

To use qsheets the user must have access to a Questrade account and setup an initial authentication token. 

1. Familiarize yourself withe the [Security Documentation](https://www.questrade.com/api/documentation/security) for the Questrade API.
2. [Generate](https://apphub.questrade.com/UI/UserApps.aspx) a manual refresh token for qsheets
3. Initialize the API with the refresh token in the main:
   
    ```python
    q = Questrade(refresh_token='XYz1dBlop33lLLuys4Bd')
    ```

    **Important**: A token will be created at ```~/.questrade.json``` and used for future API calls
      * It the token is valid future initiations will not require a refresh token
    ```python
    q = Questrade()
    ```
If for some reaon you should encounter any errors such as "token not valid" you can always go back to step 2 and generate a new refresh token on the Questrade page. Just make sure to pass the token in the inital Questrade intialization code.

### Google Account Authenication

1. Follow the [instructions](https://gspread.readthedocs.io/en/latest/oauth2.html#for-end-users-using-oauth-client-id)
2. Copy the file created in the instructions into the same directory where 'gsheets.py' resides and rename the file to ```client_key.json```

## Setup

Open ```qsheets_settings.py``` in your favourite editor and make any desired changes, in particular in regards to Google Sheets document names (see DOCS variable). qsheets will work out of the box with default settings, but the Google Sheets document will need to named 'Test1' and have 3 sheets named 'Data', 'Sparklines' and 'Returns'. These names can be modified and additional documents can also be supported. The ```qsheets_settings.py``` file is self documented.

By default, a text file ```tsx_holidays.txt``` is included that lists TSX market holidays through 2024. This file can be modified to add future dates or to modified the dates for other markets, e.g. US markets. It is recommended to create a new file and reference the file from the settings file. The format is very simple - just add dates with the format YYYY-MM-DD in each line. 

Create a Google Sheets document with the name ```Test1``` and create three sheets named ```Data```, ````Sparklines``` and ```Returns```.

**Important**: Share this document with the email that is listed in your ```client_key.json``` file created in the Google Account authentication step. Just open ```client_key.json``` in a text editor and copy the email address listed at the keyword ```client_email```. The format should be somthing like ```prjname@prjname.iam.gserviceaccount.com```. This step is crucial to allow qsheets edit access to the cells in the spreadsheet.

Finally enter a few stock symbols into column A like show here:
![before](/img/before.png)

## Usage

Open command tool (e.g. windows command prompt or power shell) and move into the folder that contains the ```qsheets.py``` file, i.e. 
```cd c:\users\johndoe\documents\qsheets``` in our example from the installation step.

Simply run the command:
```python qsheets.py``` to start the program.
The console should provide output what is happening and update the spreadsheet. By default the "Data" sheet is populated with open,high,low,close (OHLC) data. 
![after](/img/after.png)

By default the script will only run once and populate the available sheets. But the script can also be run continuously by passing the command option --continuous=True. The command would like this:
```python qsheets.py --continuous=True```. To exit the program when running in this mode hit \<Ctrl\>+C.

## Troubleshooting

* Every once in while it the Questrade API returns an error state, like "internal server error" or "symbol not found". These hiccups seem to resolve themselves fairly quickly. Better error handling and retry logic are considered as future improvements. 
* For some reason the Questrade API follows the Yahoo Finance convention for TSX Venture stocks "V" while the IQ Edge program uses the "VN" suffix. So, for GPV listed on TSXV use "GPV.V" and not "GPV.VN"

## Todo

Feel free to create pull request to improve the code and the documentation. Items that need improvement are:
- [ ] Better error handling, in particular for Questrade & Google authentication
- [ ] Build installer for gsheets
- [ ] Handle TSXV Questrade stock naming conventions
- [ ] Test with US stocks


