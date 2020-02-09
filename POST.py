import requests 
import os


url = 'https://hm1973.itp.io/image-upload'  
files = {'image_name': open('/home/pi/Desktop/surv/receipt/5-barcode.png', 'rb')}
r = requests.post(url, files=files)

print(r.status_code)
print(r.text)


