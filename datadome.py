from config.config import ua, proxy, capsolver_api_key, module_error_message

import capsolver
import requester
import json
import re

#vars
capsolver.api_key = capsolver_api_key
captcha_url = ""

def getProxy_formatted(proxy):
    return proxy.split("@")[1] + ":" + proxy.split("/")[-1].split("@")[0]

def fetchCookie(url) -> str:
    print("Fetching cookie for", url)
    r = requester.get(url)
    if r.status_code == 200:
        return None


    dd = json.loads(re.search('var dd=([^"]+)</script>', r.text).group(1).replace("'",'"'))
    initialCid = dd['cid'] 
    hsh = dd['hsh'] 
    t = dd['t']
    host = dd['host']
    cid = r.cookies['datadome'] # The request will set this cookie
    post_url = 'https://'+host+'/captcha/?initialCid={}&hash={}&cid={}&t={}'.format(initialCid, hsh, cid,t)

    # capsolver.api_key = "..."
    solution = capsolver.solve({
                "type": "DatadomeSliderTask",
                "websiteURL": url,
                "captchaUrl": post_url,
                "proxy": getProxy_formatted(proxy),
                "userAgent": ua
            })
    val = solution["cookie"][9:]
    return val


if __name__ == "__main__":
    print(__file__.split('\\')[-1],":",module_error_message)
    exit(1)