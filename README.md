# Steps 

1. Install python 
   1. Download python from https://www.python.org/downloads/
   2. Install python

2. Install pip
   1. Download get-pip.py from https://bootstrap.pypa.io/get-pip.py
   2. Open command prompt and run the following command:
      ```
      python get-pip.py
      ```

3. Install required libraries
   1. Open command prompt and run the following command:
      ```
      pip install pypdf
      ```

4. Move all the pdf files to `filesToExtract` folder

5. Run the script
   1. Open command prompt and run the following command:
      ```
      python3 process_all.py
      ```

6. The extracted output will be in the `out` folder