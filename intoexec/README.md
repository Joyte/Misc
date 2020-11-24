# intoexec
This code converts any python file into just an exec statement.
Not sure what you'd use it for, but it's there.

How to use
----------
Simply run the file, and when it asks for a file provide a valid python file path like these examples:
 - `./pyfiles/not-an-exec.py`
 - `C:\Users\longd\Documents\Python Files\also-not-exec.py`
 - `simplynotexec.py`

It will then convert it, and make a new file in the directory it was run in, with the name of the file you provided with a suffix of `-exec.py`. You can safely remove this suffix and the file will be safe :).