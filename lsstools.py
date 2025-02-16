def checkfileformat(file_path):
   """
    Checks to see if the input file is or isnt a recognised load file format.
    Currently supports .001-.009
   """
   if not file_path.endswith(tuple(f".00{i}" for i in range(1,10))):
       raise ValueError("File is not a recognised load file format")
