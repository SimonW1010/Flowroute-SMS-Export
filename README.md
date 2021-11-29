# Flowroute-SMS-Export
Exports a excel sheet with all Flowroute clients/numbers for viewing SMS billing and monitoring personal or client inbound/outbound messages

# Imports
```
import wx
import json
import os
```

# Flowroute Installation
Go to [Flowroute Github](https://github.com/flowroute/flowroute-sdk-v3-python) and download as a zip 
>
Extract zip contents 
>
Open Windows terminal (Windows + R type: cmd)
>
type ```cd C:\Users\ Location of extracted file```
>
Once you're in the proper directory type ```pip3 install -r requirements.txt```
>
Copy and paste the flowroutenumbersandmessaging folder into you're C:\Users\your user\AppData\Local\Programs\Python\Python39\Lib\site-packages directory

# Access Key / Secret Key
For line 6 you're going to need your flowroute API keys these are found here
>
Login Into Flowroute > Prefrences > API Control
>
![Screenshot 2021-11-28 155648](https://user-images.githubusercontent.com/93505099/143791617-219d24e4-5e96-4dca-a4d4-6d250a49274a.png)
>NOTE: The blue arrows point to location the red arrows point to where the API accesss keys are located

# Contacts and numbers 
Be sure the contact names are correct and the numbers correspond to the appropriate contact location on the list! 

