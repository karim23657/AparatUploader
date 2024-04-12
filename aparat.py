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
from resumable import Resumable


class ChunkedUpload:
    def __init__(self, url, token, qquuid, filename, max_byte_length=1024*1024*3, progress_callback=None):
        print('|> aa:',[url, token, qquuid, filename, max_byte_length])
        self.url = url
        self.session = requests.Session()
        self.filename = filename
        self.file_size = os.path.getsize(filename)
        self.max_byte_length = max_byte_length
        self.progress_callback = progress_callback
        self.sent_chunk_count = 0
        self.token = token 
        self.videopath = filename
        self.videoExt = str(self.videopath.rsplit(".", 1)[-1])
        self.videoName = 'test.' + self.videoExt
        self.qquuid = qquuid
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
        


    def upload(self):
        with Resumable(
            target=self.url + '/upload',
            chunk_size=self.max_byte_length,
            simultaneous_uploads=3,
            headers=self.headers,
        ) as session:
            file = session.add_file(self.filename,self.qquuid)
            file.chunk_completed.register(self.progress_callback)
        
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
        other_auth_data= parseCookieFile(cookieJar)
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
        
        u = ChunkedUpload(url=self.server_url, 
                          token=self.uploadinfo['data'][0]['attributes']['token'], 
                          qquuid=self.qquuid, 
                          filename=videopath, 
                          max_byte_length=self.max_byte_length, 
                          progress_callback=progress_callback
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
            "video_pass": "1",
            "watermark": "1",
            "category": "5",
            "comment": "yes",
            "kids_friendly": True,
            "title": title,
            "descr": description,
            "tags": "مستند-آموزشی-برچسب",
            "new_playlist": "",
            "playlist_temp": "",
            "playlistid": "",
            "subtitle": "",
            "publish_date": ""
        }
    
        response = requests.post('https://www.aparat.com/api/fa/v1/video/upload/upload/uploadId/'+self.uploadinfo['data'][0]['attributes']['uploadId'], data=json.dumps(data), cookies=self.cookies, headers=headers, verify=False)
        
        return json.loads(response.text  )

       
