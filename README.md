# woah
Automatic addition of promotional codes from the file to the website

## The script was written for fun.

**Complete the recorded data and provide correct data in script.py: _emailLogin_ and _password_.**

To run the script in the current directory, open the terminal, enter and confirm:

```py .\script.py```

### The script will select the appropriate driver for Windows, Linux or MacOS.

The script downloads promotional codes from the file. The codes can be in new lines in the file or can be separated by a separator, e.g. a comma or exclamation mark. The script checks the number of code characters (requires 12 characters) and whether it contains only alphanumeric characters - if there are different characters or non-alphanumeric characters, the script skips the code to prevent the account from being blocked if there are many wrong promotional codes. In the case of a blocked account, the script terminates the operation. For all incorrect data, the script takes a screenshot. All operations are saved to the file *logs.txt* which is automatically created.
