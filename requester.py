from config.config import ua, proxy, module_error_message
import requests
import json

# functions
def spoofTLS(requests):
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

spoofTLS(requests)

def get(url, dd_cookie=None) -> requests.Response:
    if dd_cookie == None:
        return requests.get(url, headers={"User-Agent":ua}, proxies={"http":proxy, "https":proxy})
    else:
        return requests.get(url, headers={"User-Agent":ua}, proxies={"http":proxy, "https":proxy}, cookies={"datadome":dd_cookie})

def getHtml(url:str, dd_cookie:str) -> (str,int):
    #cookie format
    try:
        res = get(url, dd_cookie=dd_cookie)
        return res.text, res.status_code
    except:
        print("Error in getHtml")
        return None, None

if __name__ == "__main__":
    print(__file__.split('\\')[-1],":",module_error_message)
    exit(1)
    
res = get("https://api.myip.com")
ip = json.loads(res.text)["ip"]
print("Scrapper with IP:", ip)