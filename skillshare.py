import requests, json, sys, re, os
from slugify import slugify

class Skillshare(object):

    def __init__(
        self,
        cookie,
        download_path=os.environ.get('FILE_PATH', './Skillshare'),
        pk='BCpkADawqM2OOcM6njnM7hf9EaK6lIFlqiXB0iWjqGWUQjU7R8965xUvIQNqdQbnDTLz0IAO7E6Ir2rIbXJtFdzrGtitoee0n1XXRliD-RH9A-svuvNW9qgo3Bh34HEZjXjG4Nml4iyz3KqF',
        brightcove_account_id=615938610,
    ):
        self.cookie = """ device_session_id=849d2d6a-dd88-42bf-bb0e-0d6223b9fb2e; show-like-copy=1; first_landing=utm_campaign%3D%26utm_source%3D%28direct%29%26utm_medium%3D%28none%29%26referrer%3D%26referring_username%3D; _gcl_au=1.1.357138047.1598957785; sm_uuid=1598958618918; __pdst=7fcb13c2d6f34e54b8f45d41929c2e3e; _scid=ec0681c2-1b5a-490f-ad88-ba497ba465cc; __stripe_mid=d17e4fc6-4942-4ba3-bf15-3af9d68e75ddd0b80e; __qca=P0-188086976-1598957788870; __ssid=a5749bc6b3f91690f60441f0815ae9e; _sctr=1|1598889600000; G_ENABLED_IDPS=google; skillshare_user_=fdebef234c2ca6cf87d78aa01ad0ee8bebfc00efa%3A4%3A%7Bi%3A0%3Bs%3A8%3A%2214695449%22%3Bi%3A1%3Bs%3A20%3A%22kikoxi6023%40qlenw.com%22%3Bi%3A2%3Bi%3A2592000%3Bi%3A3%3Ba%3A11%3A%7Bs%3A5%3A%22email%22%3Bs%3A20%3A%22kikoxi6023%40qlenw.com%22%3Bs%3A9%3A%22firstName%22%3Bs%3A4%3A%22Jane%22%3Bs%3A8%3A%22lastName%22%3Bs%3A9%3A%22Nazarudin%22%3Bs%3A8%3A%22headline%22%3BN%3Bs%3A3%3A%22pic%22%3Bs%3A68%3A%22https%3A%2F%2Fstatic.skillshare.com%2Fassets%2Fimages%2Fdefault-profile-2020.jpg%22%3Bs%3A5%3A%22picSm%22%3Bs%3A68%3A%22https%3A%2F%2Fstatic.skillshare.com%2Fassets%2Fimages%2Fdefault-profile-2020.jpg%22%3Bs%3A5%3A%22picLg%22%3Bs%3A68%3A%22https%3A%2F%2Fstatic.skillshare.com%2Fassets%2Fimages%2Fdefault-profile-2020.jpg%22%3Bs%3A9%3A%22isTeacher%22%3Bs%3A1%3A%220%22%3Bs%3A8%3A%22username%22%3Bs%3A9%3A%22615938610%22%3Bs%3A3%3A%22zip%22%3BN%3Bs%3A6%3A%22cityID%22%3Bs%3A1%3A%220%22%3B%7D%7D; __utmv=99704988.|1=visitor-type=user=1; _pin_unauth=dWlkPVpXUXpNek0xTWprdE56STJPUzAwTVdGaExXRTFOelV0TTJOalpHRTFOamN6WkRaaCZycD1abUZzYzJV; PHPSESSID=10b34e126c839d1325f4d8d82429609c; YII_CSRF_TOKEN=VTQ5UzBvcEZZc2QzZEo5ek0xTHNQbmMyUUljMEN1bHg6-9AKin2YS-dW0ItB85JYi1cTKlVEKLRkYoOEL4B0CQ%3D%3D; __stripe_sid=ddb4df93-226a-4a44-aeca-1b1fa845f7fa8aea11; ss-ref=%7B%22teacher%22%3A%7B%226595003%22%3A%7B%22classId%22%3Anull%2C%22referralType%22%3A%22affiliate%22%7D%7D%7D; visitor_tracking=utm_campaign%3D269814%26utm_source%3DIR%26utm_medium%3Daffiliate-referral%26referrer%3D%26referring_username%3D; __utma=99704988.1230507541.1598957786.1598975773.1599020259.4; __utmc=99704988; __utmz=99704988.1599020259.4.4.utmcsr=IR|utmccn=269814|utmcmd=affiliate-referral|utmctr=Online%20Tracking%20Link|utmcct=4650; IR_gbd=skillshare.com; _uetsid=7d37258ccc7d68ec12a7e97512abd089; _uetvid=b2f3699a1edb4f22f5d9aa1a73b3754c; IR_PI=c6ca7dcd-ec41-11ea-9dae-42010a24630a%7C1599106662392; IR_4650=1599020262392%7C-1%7C1599020258899%7CQDWyaVXZxxyORfPwUx0Mo3QWUkiVgJVIORv2280%7C; __utmb=99704988.2.10.1599020259; CAPTIONS=off; ss-subscription-coupon=referral2m
"""
        self.download_path = download_path
        self.pk = pk.strip()
        self.brightcove_account_id = brightcove_account_id
        self.pythonversion = 3 if sys.version_info >= (3, 0) else 2

    def is_unicode_string(self, string):
        if (self.pythonversion == 3 and isinstance(string, str)) or (self.pythonversion == 2 and isinstance(string, unicode)):
            return True

        else:
            return False

    def download_course_by_url(self, url):
        m = re.match('https://www.skillshare.com/classes/.*?/(\\d+)', url)
        assert m, 'Failed to parse class ID from URL'
        self.download_course_by_class_id(m.group(1))

    def download_course_by_class_id(self, class_id):
        data = self.fetch_course_data_by_class_id(class_id=class_id)
        teacher_name = None
        if 'vanity_username' in data['_embedded']['teacher']:
            teacher_name = data['_embedded']['teacher']['vanity_username']
        if not teacher_name:
            teacher_name = data['_embedded']['teacher']['full_name']
        assert teacher_name, 'Failed to read teacher name from data'
        if self.is_unicode_string(teacher_name):
            teacher_name = teacher_name.encode('ascii', 'replace')
        title = data['title']
        if self.is_unicode_string(title):
            title = title.encode('ascii', 'replace')
        base_path = os.path.abspath(os.path.join(self.download_path, slugify(teacher_name), slugify(title))).rstrip('/')
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        for u in data['_embedded']['units']['_embedded']['units']:
            for s in u['_embedded']['sessions']['_embedded']['sessions']:
                video_id = None
                if 'video_hashed_id' in s:
                    if s['video_hashed_id']:
                        video_id = s['video_hashed_id'].split(':')[1]
                    assert video_id, 'Failed to read video ID from data'
                    s_title = s['title']
                    if self.is_unicode_string(s_title):
                        s_title = s_title.encode('ascii', 'replace')
                    file_name = '{} - {}'.format(str(s['index'] + 1).zfill(2), slugify(s_title))
                    self.download_video(fpath='{base_path}/{session}.mp4'.format(base_path=base_path,
                      session=file_name),
                      video_id=video_id)
                    print('')

    def fetch_course_data_by_class_id(self, class_id):
        res = requests.get(url=('https://api.skillshare.com/classes/{}'.format(class_id)),
          headers={'Accept':'application/vnd.skillshare.class+json;,version=0.8',
         'User-Agent':'Skillshare/4.1.1; Android 5.1.1',
         'Host':'api.skillshare.com',
         'cookie':self.cookie})
        assert res.status_code == 200, 'Fetch error, code == {}'.format(res.status_code)
        return res.json()

    def download_video(self, fpath, video_id):
        meta_url = 'https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{video_id}'.format(account_id=(self.brightcove_account_id),
          video_id=video_id)
        meta_res = requests.get(meta_url,
          headers={'Accept':'application/json;pk={}'.format(self.pk),
         'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
         'Origin':'https://www.skillshare.com'})
        assert not meta_res.status_code != 200, 'Failed to fetch video meta'
        for x in meta_res.json()['sources']:
            if 'container' in x:
                if x['container'] == 'MP4' and 'src' in x:
                    dl_url = x['src']
                    break

        print('Downloading {}...'.format(fpath))
        if os.path.exists(fpath):
            print('Video already downloaded, skipping...')
            return
        with open(fpath, 'wb') as (f):
            response = requests.get(dl_url, allow_redirects=True, stream=True)
            total_length = response.headers.get('content-length')
            if not total_length:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write('\r[%s%s]' % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()

            print('')
