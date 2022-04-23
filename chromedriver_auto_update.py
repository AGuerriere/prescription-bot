# This is needed to find the version of the chromedriver inside brew
import subprocess
import os

# the following code is used to find the path of the chromedriver installed through homebrew
output = subprocess.check_output(['brew', 'info', 'chromedriver']) # this is used to run terminal commands and read the output in python
output_string = output.decode("utf-8") #the output is of type bytes, and to be transformed in a string it needs to be decoded
# splitting the output string to get the chromedriver version number
first_split = output_string.split(' ')[1]
second_split = first_split.split('chromedriver/')
version = second_split[1]

# grant permission to chromedriver to fix error message: "Fixing error: “chromedriver” cannot be opened because the developer cannot be verified. Unable to launch the chrome browser on Mac OS"
os.system('xattr -d com.apple.quarantine /usr/local/Caskroom/chromedriver/'+ version + '/chromedriver')

# chromedriver path
PATH = '/usr/local/Caskroom/chromedriver/'+ version + '/chromedriver'