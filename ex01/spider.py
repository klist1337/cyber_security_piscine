
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import os

VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
visited_urls = set()
def is_valid_image(url:str):
  return any(url.lower().endswith(ext) for ext in VALID_EXTENSIONS)

# crawl into the url with depth level input default=5
def crawl(max_depth:int, url:str, output_path:str, current_depth=0) :
   if current_depth > max_depth or url in visited_urls :
      return
   visited_urls.add(url)
   extract_image(url, output_path)
   try:
      soup = BeautifulSoup(requests.get(url).text, 'html.parser')
      for link in soup.find_all('a', href=True) :
         next_url = urljoin(url, link['href'])
         if (urlparse(next_url).netloc == urlparse(url).netloc):
            crawl(max_depth, next_url, output_path, current_depth + 1)
   except Exception as e :
         print(f"failed to download image at level {current_depth}")
def download_image(url:str, output_path:str):
   #request to get the content
   try :
      r = requests.get(url, stream=True, timeout=10)
      # raise HttpError
      r.raise_for_status()
      
      # get the file name 
      file_name = os.path.basename(urlparse(url).path)
      full_path = os.path.join(output_path, file_name)
      print(full_path)
      # openfile and put binary data inside
      with open(full_path, 'wb') as f:
        # to avoid downloading content at once in memory for larges responses 
        for chunk in r.iter_content(1024) :
           f.write(chunk)
           print(f"Downloaded {url}")
   except Exception as e:
        print(f"failed to download {url}: {e}")



def extract_image(url:str, output_path:str) :

   try :
      r = requests.get(url)
      # get all images tag in html 
      soup = BeautifulSoup(r.text, 'html.parser')   
      images = soup.find_all('img')
      # iterate in each image to join url to the source
      for img in images :
         src = img.get('src')
         if src :
            img_url = urljoin(url, src)
            if is_valid_image(img_url):
               download_image(img_url, output_path)
               # print(img_url)
   except Exception as e :
      print(f"Failed to access {url} : {e}")

def main() :
   
   # Parse argument
   parser = argparse.ArgumentParser()
   # add positional argument 
   parser.add_argument('url',help="url to download image")
   # add optional argument
   parser.add_argument('-r', action="store_true", help="recursive download")
   parser.add_argument('-l', default=5, type=int, help="depth level of recursive download")
   parser.add_argument('-p', default="./data/", type=str, help="path to store downloaded images")
   args = parser.parse_args()

   # create a directory for to save image
   # parents=True to create parent / exist_ok=True 
   # to not fail is the Directory exist
   Path(args.p).mkdir(parents=True, exist_ok=True)
   if args.r :
       crawl(args.l, args.url, args.p)
   else:
      extract_image(args.url, args.p)
   # make a request in the website
   

if __name__ == "__main__" :
   main()
   