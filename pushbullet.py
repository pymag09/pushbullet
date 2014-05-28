__author__ = 'Bieliaievskyi Sergey'
__credits__ = ["Bieliaievskyi Sergey"]
__license__ = "Apache License"
__version__ = "1.0.0"
__maintainer__ = "Bieliaievskyi Sergey"
__email__ = "magelan09@gmail.com"
__status__ = "Release"

import urllib.parse
import mimetypes
import base64
import pycurl
import json
import io


class PushBullet:
    def __init__(self, api_id):
        self.auth_id = api_id
        self.post_data = {}
        self.main_url = 'https://api.pushbullet.com/v2/'

    def pb_request(self, url, req_method=None):
        curl_obj = pycurl.Curl()
        response = io.BytesIO()
        encoded_string = base64.encodebytes(('%s:' % self.auth_id).encode())[:-1]
        auth = "Basic %s" % encoded_string.decode('utf-8')
        if self.post_data:
            req_data = json.dumps(self.post_data)
            curl_obj.setopt(curl_obj.POSTFIELDS, req_data)
        if req_method:
            curl_obj.setopt(pycurl.CUSTOMREQUEST, req_method)
        curl_obj.setopt(pycurl.URL, url)
        curl_obj.setopt(curl_obj.WRITEFUNCTION, response.write)
        curl_obj.setopt(curl_obj.HTTPHEADER, ["Authorization: %s" % auth,
                                              "Accept: application/json",
                                              "Content-Type: application/json",
                                              "User-Agent: PushBullet-agent"])
        curl_obj.perform()
        return curl_obj.getinfo(pycurl.HTTP_CODE), \
               curl_obj.getinfo(pycurl.EFFECTIVE_URL), \
               json.loads(response.getvalue().decode())


class PBFileUpload(PushBullet):
    def __init__(self, api_key_id):
        PushBullet.__init__(self, api_key_id)
        self.file_upload_param = {}

    def upload_request(self, file_name):
        url_param = urllib.parse.urlencode({'file_name': file_name, 'file_type': mimetypes.guess_type(file_name)[0]})
        self.file_upload_param = self.pb_request('%supload-request?%s' % (self.main_url, url_param))[2]

    def pb_upload(self, file_path):
        buffer = io.BytesIO()
        data = [(elm, str(val)) for (elm, val) in self.file_upload_param['data'].items()]
        data.append(('file', (pycurl.FORM_FILE, file_path)))
        my_curl = pycurl.Curl()
        my_curl.setopt(pycurl.URL, self.file_upload_param['upload_url'])
        my_curl.setopt(pycurl.HTTPPOST, data)
        my_curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
        my_curl.perform()
        return my_curl.getinfo(pycurl.HTTP_CODE), \
               my_curl.getinfo(pycurl.EFFECTIVE_URL)


class PBUsers(PushBullet):
    def __init__(self, api_key_id):
        PushBullet.__init__(self, api_key_id)

    def get_me(self):
        return self.pb_request('%susers/me' % self.main_url)


class PBContacts(PushBullet):
    def __init__(self, api_key_id):
        PushBullet.__init__(self, api_key_id)

    def get_contacts(self):
        return self.pb_request('%scontacts' % self.main_url)

    def del_contact(self, contact_iden):
        return self.pb_request('%scontacts/%s' % (self.main_url, contact_iden), req_method='DELETE')


class PBDevices(PushBullet):
    def __init__(self, api_key_id):
        PushBullet.__init__(self, api_key_id)

    def get_connected_devices(self):
        return self.pb_request('%sdevices' % self.main_url)

    def del_connected_device(self, dev_id):
        return self.pb_request('%sdevices/%s' % (self.main_url, dev_id), req_method='DELETE')


class PBPushes(PushBullet):
    def __init__(self, api_key_id):
        PushBullet.__init__(self, api_key_id)

    def get_push_history(self):
        return self.pb_request('%spushes?modified_after=0' % self.main_url)

    def del_pushes(self, push_id):
        return self.pb_request('%spushes/%s' % (self.main_url, push_id), req_method='DELETE')

    def pushes(self, **pbargs):
        self.post_data = pbargs
        return self.pb_request('%spushes' % self.main_url)