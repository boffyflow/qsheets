# qsheets
Questrade to Google Sheets bridge

## Introduction

qsheets is a simple python script that allows to retrieve stock market data from Questrade through it's REST API and populate one or multipe Google Sheets documents automatically.

## Pre-requistites

### Questrade Account Authenication

To use qsheets the user must have access to a Questrade account and setup an initial authentication token. 

1. Familiarize yourself withe the [Security Documentation](https://www.questrade.com/api/documentation/security) for the Questrade API.
2. [Generate](https://login.questrade.com/APIAccess/UserApps.aspx) a manual refresh token for qsheets
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

## Installation

## Setup

## Usage

Open command tool (e.g. windows command prompt or power shell)

## Troubleshooting

## Todo

- [ ] Better error handling, in particular for Questrade & Google authentication


