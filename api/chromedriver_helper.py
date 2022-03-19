import os, subprocess, re,  requests, unicodedata, tempfile, io;

from lxml import html

class ChromedriverHelper():
	def __init__(self):
		# Aqui neste ponto está forçando para um GNU/Linux, se for usar windows, cofirme
		#   se é google-chrome o comando no Windows
		p = subprocess.Popen(["google-chrome", "--version"], stdout=subprocess.PIPE);
		saida = p.communicate()[0];
		self.version = re.search("[0-9]{1,3}", str(saida))[0];
		self.path = "/tmp/chromedriver";
		if not os.path.exists(self.path):
			self.chromedriver_download();
	
	def download_file(self, url):
		path_to_download = tempfile.gettempdir() + "/chromedriver.zip";
		with requests.get(url, stream=True) as r:
			r.raise_for_status();
			with open( path_to_download , 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192): 
					f.write(chunk);
		return path_to_download;
	
	def ofuscar(self, path_chromedriver):
		replacement = "abc_roepstdlwoeproslPOweos".encode()
		with io.open(path_chromedriver, "r+b") as fh:
			for line in iter(lambda: fh.readline(), b""):
				if b"cdc_" in line:
					fh.seek(-len(line), 1);
					newline = re.sub(b"cdc_.{22}", replacement, line);
					fh.write(newline);
					
	def chromedriver_download(self):
		# Primeiro passo é obter o link para download da versão/subversão corrente
		page = requests.get("https://chromedriver.chromium.org/downloads");
		page.encoding = "utf-8";
		tree = html.fromstring(unicodedata.normalize(u'NFKD', page.text).encode('ascii', 'ignore').decode('utf8'));
		links = tree.xpath("//a[contains(@href, 'path="+ self.version +".')]");
		VERSAO_CROMEDRIVE_SITE = re.findall("[0-9.]+", links[0].attrib.get("href") );

		# montando a URL para download do Chromedrive do GNU/Linux 64bits
		#     para windows, montar um caminho de URL diferente de linux
		link_download =  "https://chromedriver.storage.googleapis.com/" + VERSAO_CROMEDRIVE_SITE[-1] + "/chromedriver_linux64.zip";
		path_to_download = self.download_file(link_download);

		# Agora que o DOWNLOAD está feito, vamos descompactar e movimentar o arquivo resultante
		#   precisa do unzip instalado.
		subprocess.run(["unzip", path_to_download , "-d", tempfile.gettempdir() + os.sep ]);
		self.ofuscar("/tmp/chromedriver");

