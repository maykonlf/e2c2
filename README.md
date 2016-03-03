# e2c2 - Easy EC2

For easily management of EC2 users. Create, delete and authorise user for each instance from a google spreadsheet.

### Dependencies
- Python 2.7
- pip2
- Run ```pip2 install -r requirements.txt``` to install the needed libraries
### Instructions
1. Create an Google Spreadsheet following [this model](https://docs.google.com/spreadsheets/d/1CNil72LQPxAd6lVEOLNIWesqouGBMw4IFjNtiychxCU/edit?usp=sharing) 
2. Create an Google Drive Credential on Google Console 
3. Select Service Account Key -> New Service Account -> Fill the fields with needed info -> Select JSON -> Click on "Create" and save the JSON file in some place safe
4. Add the following lines to your `~/.bashrc` file:
```bash
export CREDENTIALS_PATH="/somesirectory/api-a8016.json" 
export PEM_DIR="/somedirectory/PEM/"
```
5. Run `python __init__.py`
6. And it's done

Any trouble open an issue :wink:
