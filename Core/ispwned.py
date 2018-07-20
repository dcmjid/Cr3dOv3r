#Written by: Karim shoair - D4Vinci ( Cr3dOv3r )
import requests
from .color import *

UserAgent = {'User-Agent': 'Cr3dOv3r-Framework'}
def check_haveibeenpwned(email):
    #from haveibeenpwnd API docs from https://haveibeenpwned.com/API/v2#BreachesForAccount
    url = "https://haveibeenpwned.com/api/v2/breachedaccount/"+str(email)
    req = requests.get(url, headers=UserAgent)
    if req.status_code==200:
        return req.json()
    else:
        return False

def grab_password(email):
     url  = "https://ghostproject.fr/search.php"
     data = {"param":email}
     req = requests.post(url,headers=UserAgent,data=data)
     result = req.text.split("\\n")
     if len(result)==1:
         return False
     else:
         return result[1:-1]

def parse_data(email,np):
    data = check_haveibeenpwned(email)
    if not data:
        error("No leaks found in Haveibeenpwned website!")
    else:
        status("Haveibeenpwned website results: "+Y+str(len(data)))
        form  = "Name : {web} | Date : {date} | What leaked : {details}"
        for website in data:
            line = form.format(web=M+website["Name"]+B,date=M+website["AddedDate"]+B,details=M+",".join(website["DataClasses"])+B)
            status(B+line)
        if not np:
            p = grab_password(email)
            if p:
                status("Plaintext passwords found!")
                for pp in p:
                    print(C+" │"+B+"  └──── "+W+pp.split(":")[1])
            else:
                error("Didn't find any plaintext password published!")
