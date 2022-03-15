import tempfile, os, hashlib, json, datetime, unicodedata, requests, random;
from lxml import html

class CacheRequest():
    # life em minutos....
    def __init__(self, life=1, cache=True):
        self.cache = cache;
        self.life = life;
        self.VERSION = "2";
        self.text = None;
        self.tree = None;
   
    def get(self, url):
        PATH_TO_CACHE_FILE = os.path.join(tempfile.gettempdir(),  hashlib.md5( url.encode() ).hexdigest() + self.VERSION  );
        if self.cache:
            if os.path.exists(PATH_TO_CACHE_FILE):
                buffer = json.loads( open(PATH_TO_CACHE_FILE, "r").read() );
                if datetime.datetime.utcnow() < datetime.datetime.strptime(buffer["data"], '%Y-%m-%d %H:%M:%S'  ):
                    self.text = buffer["html"];
                    self.tree = html.fromstring(self.text);
                    return True;
        agentes = [ "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36" ,
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.63",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0",
          "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
          "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        ];
        req = requests.Session();
        page = req.get(url, headers = {'User-Agent': agentes[random.randint(0, 5)]});
        #page = requests.get(url, headers = {'User-Agent': agentes[random.randint(0, 5)]});
        page.encoding = "utf-8";
        self.text = unicodedata.normalize(u'NFKD', page.text).encode('ascii', 'ignore').decode("utf-8");
        self.tree = html.fromstring(self.text); 
        if self.cache:
            with open(PATH_TO_CACHE_FILE, 'w') as f:
                f.write(json.dumps({"data" : (datetime.datetime.utcnow() + datetime.timedelta(minutes=self.life)).strftime('%Y-%m-%d %H:%M:%S') , "html" : self.text}));
                f.close();
        return True;
    def elements(self, xpath):
        return self.tree.xpath(xpath);
    def element(self, xpath):
        buffer = self.elements(xpath);
        if buffer != None and len(buffer) > 0:
            return buffer[0];
        return None;