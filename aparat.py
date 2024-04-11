import re, requests


from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def parseCookieFile(cookiefile):
    """Parse a cookie .txt file and return a dictionary of key value pairs compatible with requests."""
    cookies = {}
    with open(cookiefile, 'r') as fp:
        for line in fp:
            # Ignore comments and empty lines
            line=line.replace("#HttpOnly_",'').replace("\n",'')
            if not re.match(r'^\s*#', line) and not re.match(r'^\s*$', line):
                # Extract the cookie attributes
                domain, flag, path, secure, expiration, name, value = re.findall(r'[^ \t]+', line)
                # Convert the expiration time to an integer
                expiration = int(expiration)
                # Ignore session cookies
                if expiration != 0:
                    # Create a cookie object
                    cookie = requests.cookies.create_cookie(domain=domain, name=name, value=value)
                    # Set the cookie attributes
                    cookie.secure = (secure == 'TRUE')
                    cookie.expires = expiration
                    cookie.path = path
                    # Add the cookie to the dictionary
                    cookies[cookie.name] = cookie.value
    return cookies




import os
from concurrent.futures import ThreadPoolExecutor

class ChunkedUpload:
    def __init__(self, url, token, qquuid, filename, max_byte_length=1024*1024*3, progress_callback=None ,num_workers=3):
        self.url = url
        self.session = session
        self.filename = filename
        self.file_size = os.path.getsize(filename)
        self.max_byte_length = max_byte_length
        self.progress_callback = progress_callback
        self.sent_chunk_count = 0
        self.token = token 
        self.videopath = filename
        self.videoExt = str(self.videopath.rsplit(".", 1)[-1])
        self.videoMime = what_the_mime('.'+self.videoExt)
        self.videoName = 'test.' + self.videoExt
        self.qquuid = qquuid
        self.num_workers = num_workers
        
        self.chunk_list = [(start, min(start + self.max_byte_length, self.file_size)) for start in range(0, self.file_size, self.max_byte_length)]
        self.totalparts = len(self.chunk_list)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.aparat.com/',
            'X-Token': self.token,
            'Origin': 'https://www.aparat.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }
        
    def upload_chunk(self, chunk):
        start, end = chunk
        with open(self.filename, 'rb') as file:
            file.seek(start)
            chunk_data = file.read(end - start)

        chunk_size = min(end - start, self.max_byte_length)
        data = {
            "qqpartindex": self.sent_chunk_count,
            "qqchunksize": chunk_size,
            "qqpartbyteoffset": start,
            "qqtotalfilesize": self.file_size,
            "qqtype": self.videoMime,
            "qquuid": self.qquuid,
            "qqfilename": self.videoName,
            "qqfilepath": self.videoName,
            "qqtotalparts": self.totalparts,
        }
        self.sent_chunk_count += 1
        print("|> snt data:", data)
        files = {'qqfile': chunk_data}
        response = self.session.post(self.url + '/upload', data=data, files=files, headers=self.headers, verify=False)

        if response.status_code != 200:
            raise Exception("Upload failed with status code {}".format(response.status_code))
        else:
            print(self.sent_chunk_count, response.text)
            ssss= start

        if self.progress_callback:
            progress = (start + self.max_byte_length) / self.file_size
            self.progress_callback(progress)
        
        

    def upload(self):
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:  # Increase the max_workers value
            list(executor.map(self.upload_chunk, self.chunk_list))
            
        response = self.session.get(self.url + '/file/' + self.qquuid, verify=False)
        print("|> Ax1:", response.text)
        data = {
            'qquuid': self.qquuid,
            'qqfilename': self.videoName,
            'qqtotalfilesize': self.file_size,
            'qqtotalparts': self.totalparts,
        }
        response = self.session.post(self.url + '/chunksdone', data=data, headers=self.headers, verify=False)

import json
import uuid
import math
import time


def what_the_mime(extn):
    allmimes=[{"ext": "video/x-matroska","mime": ".mkv"},{"ext": "video/3gpp","mime": ".3gp"},{"ext": "video/mp4","mime": ".mp4"},{"ext": "video/mp4","mime": ".m4p"},{"ext": "video/mp4","mime": ".m4b"},{"ext": "video/mp4","mime": ".m4r"},{"ext": "video/mp4","mime": ".m4v"},{"ext": "video/mpeg","mime": ".m1v"},{"ext": "video/ogg","mime": ".ogg"},{"ext": "video/quicktime","mime": ".mov"},{"ext": "video/quicktime","mime": ".qt"},{"ext": "video/webm","mime": ".webm"},{"ext": "video/x-m4v","mime": ".m4v"},{"ext": "video/ms-asf","mime": ".asf"},{"ext": "video/ms-asf","mime": ".wma"},{"ext": "video/x-ms-wmv","mime": ".wmv"},{"ext": "video/x-msvideo","mime": ".avi"}]
    for x in allmimes:
        if x['mime']==extn:
            return x['ext']



class AparatUploader():
    def __init__(self,cookieJar):
        # self.videopath = videopath
        # self.videoExt= str(videopath.rsplit(".", 1)[-1])
        # self.videoMime = what_the_mime(self.videoExt)
        # self.videoName='test.'+self.videoExt
        self.max_byte_length=3000000#1024*1024*3#
        # Create a session object
      
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.aparat.com/uploadvideo',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }
        other_auth_data= parseCookieFile('cookies.txt')
        self.cookies = {
            'AuthV1': other_auth_data['AuthV1'],
            '_ga': other_auth_data['_ga'],
            'AFCN': other_auth_data['AFCN'],
            'm_id': other_auth_data['m_id'],
            '_ym_uid': other_auth_data['_ym_uid'],
            '_ym_d': other_auth_data['_ym_d'],
            'ads_row': '5',
            '_clck': other_auth_data['_clck'],
            'lang': 'fa',
            '_ym_isad': '1',
        }
        
    def _get_upload_info(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.aparat.com/uploadvideo',
            'isNext': 'true',
            'jsonType': 'simple',
            'domain': 'aparat',
            'currentUrl': 'https://www.aparat.com/uploadvideo',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.aparat.com/upload',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.aparat.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        }
        
        response =  requests.get('https://www.aparat.com/api/fa/v1/video/upload/upload_config', cookies=self.cookies, headers=headers,verify=False)
        uploadinfo_1=json.loads(response.text  )
        # print(response.text)
        qquuid=str(uuid.uuid4())
        self.server_url=uploadinfo_1['data']['server']
        self.qquuid=qquuid
        data = {"uploadIds":[self.qquuid],"upload_base_url":self.server_url,"upload_cnt":1}
        response =  requests.post('https://www.aparat.com/api/fa/v1/video/upload/upload_url',data=json.dumps(data), cookies=self.cookies, headers=headers1,verify=False)
        print(">>>> data:",data)
        print(">>>> data:",json.dumps(data))
        self.uploadinfo=json.loads(response.text  )
        print(">>>> uploadinfo:",self.uploadinfo)
        return self.uploadinfo
    
    def upload_video(self,videopath, progress_callback=None):
        self._get_upload_info()
        u = ChunkedUpload( self.server_url, 
                          self.uploadinfo['data'][0]['attributes']['token'], 
                          self.qquuid, 
                          videopath, 
                          self.max_byte_length, 
                          progress_callback
                         )
        u.upload()
    def upload(self ,
               videopath,
               title="عنوان",
               description="توضیخات",
               progress_callback=None):
        self.upload_video(videopath, progress_callback)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.aparat.com/uploadvideo',
            'Content-Type': 'application/json; charset=utf-8',
            'isNext': 'true',
            'jsonType': 'simple',
            'domain': 'aparat',
            'currentUrl': 'https://www.aparat.com/uploadvideo',
            'Origin': 'https://www.aparat.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        data = {
            "uploadId": self.uploadinfo['data'][0]['attributes']['uploadId'],
            "upload_base_url": self.server_url,
            "video": self.qquuid,
            "video_pass": 1,
            "watermark": "yes",
            "watermark_bool": True,
            "category": "5",
            "comment": "yes",
            "kids_friendly": False,
            "title": title,
            "descr": description,
            "tags": "مستند-آموزشی-برچسب",
            "new_playlist": "",
            "playlist_temp": "",
            "playlistid": [],
            "subtitle": [],
            "subtitle_temp": [],
            "publish_date": None
        }
    
        response = requests.post('https://www.aparat.com/api/fa/v1/video/upload/upload/uploadId/'+self.uploadinfo['data'][0]['attributes']['uploadId'], data=json.dumps(data), cookies=self.cookies, headers=headers, verify=False)
        
        return json.loads(response.text  )

       
