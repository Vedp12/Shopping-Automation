import os

price_filtering = int(input("Enter the price to starts withs "))
def filtring_files(files):
   if os.path.isfile(files):
      # print(f"'{files}' is a file.")
      with open(files,"r" ,encoding="UTF-8") as f:
         title = f.readline()
         prices = f.readline()
         format_price = prices[7:16].replace(",","")
         if int(format_price)<int(price_filtering):
            print(f"{title} {prices} {f.read()}")
         # print(format_price)
   elif os.path.isdir(files):
      # print(f"'{files}' is a directory.")
      
      allfiles = os.listdir(files)
      for allfile in allfiles:
            filtring_files(os.path.join(files,allfile))
            
   else:
      print(f"'{files}' does not exist.")
   
filtring_files("Products")