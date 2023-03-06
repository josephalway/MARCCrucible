Dear Reader,

MARC Crucible is a command Line tool that uses pymarc (https://pypi.org/project/pymarc/) to search for and save matched records.

This was developed on Windows 10 in PyCharm. It may or may not work in Linux. I don't recall, if I've ever tested it.

The input file should be a valid MARC format file. Saved records are saved in MARC format, 
so naming the saved file something similar to MySearchResults.mrc is a good idea.

Use RegEx Searches at your own peril. In the event that you have no idea what you're doing. I'm sure you could do some bad things. 
Or even in the event that you do know what you're doing. You have been warned. Still, RegEx is very powerful and useful.

This is definitely more of a beta version of the tool, but it's very usable. At least for me it is, hopefully it will be for you as well.

There's no real rhyme or reason for the various features other than, my own needs.

In the event that your Integrated Library System wants to charge you for reports, is stupidly complex, or just doesn't have it's act together.
This tool can be very helpful in finding typos, errors, or compiling a list of records that may not be easy to get without a third-party tool such as this one.

The .spec file is an example pyinstaller spec file that you can use to compile the program into a windows executable. Please note, you will need to remove or modify the icon entry, but I left it in as a useful suggestion. As far as I understand it you will need to install the Windows 10 SDK, if you want to compile the program using pyinstaller. This program is dependent on pymarc actually being functional and was tested with v.4.1.3 of pymarc.

Sincerely,
The Author
