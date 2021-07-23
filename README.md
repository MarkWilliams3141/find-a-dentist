# Find a dentist
A simple tool to find NHS dentists taking on new NHS patients.

* Search for NHS dentists near a given postcode
* Write results to log file

# Before You Begin
1. [Install python3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/).
2. [Download chomedriver.exe](https://sites.google.com/a/chromium.org/chromedriver/downloads) into the `driver` directory. 
3. Install dependencies with the `pip install -r requirements.txt` command.

# Usage
Run `python find-a-dentist.py` from the terminal to execute the script. If the `--postcode` argument is missing you will be prompted for a postcode. Use `-l` or `--logging` to save results in the `/results` directory.



```
usage: find-a-dentist.py [-h] [-l] [-s] [-p POSTCODE]

optional arguments:
  -h, --help                            show this help message and exit
  -l, --logging                         logging mode, save results
  -s, --silent                          hide console output
  -p POSTCODE, --postcode POSTCODE      postcode for search area
```
