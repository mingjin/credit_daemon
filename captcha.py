# -*- coding: utf-8 -*-

from PIL import Image
import sys, hashlib, os, random, urllib, urllib2
from datetime import *
from lxml import etree


class CaptchaResolver(object):

    def http_request(self, url, paramDict):
        post_content = ''
        for key in paramDict:
            post_content = post_content + '%s=%s&' % (key, paramDict[key])
        post_content = post_content[0:-1]
        # print post_content
        req = urllib2.Request(url, data=post_content)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, post_content)
        return response.read()

    def http_upload_image(self, url, paramKeys, paramDict, filebytes):
        timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        boundary = '------------' + hashlib.md5(timestr).hexdigest().lower()
        boundarystr = '\r\n--%s\r\n' % (boundary)

        bs = b''
        for key in paramKeys:
            bs = bs + boundarystr.encode('ascii')
            param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s" % (key, paramDict[key])
            # print param
            bs = bs + param.encode('utf8')
        bs = bs + boundarystr.encode('ascii')

        header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n' % (
            'sample')
        bs = bs + header.encode('utf8')

        bs = bs + filebytes
        tailer = '\r\n--%s--\r\n' % (boundary)
        bs = bs + tailer.encode('ascii')

        import requests
        headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
                   'Connection': 'Keep-Alive',
                   'Expect': '100-continue',
                   }
        response = requests.post(url, params='', data=bs, headers=headers)
        return response.text

    
    def get_captcha_image(self, original):
        left = 295 #location['x']
        top = 375 #location['y'] + 100
        right = 395 #location['x'] + size['width']
        bottom = 400 #location['x'] + size['height'] + 100

        image = Image.open(original)
        image = image.crop((left, top, right, bottom))
        rgb_image = image.convert("RGB")
        return rgb_image

    def get_captcha_value(self, result):
        tree = etree.XML(result)
        return tree.xpath("//Result/text()")[0]

    def resolve_captcha(self, imagePath):
        paramDict = {}
        result = ''
        paramDict['username'] = 'skyairmj'
        paramDict['password'] = '70493763'
        paramDict['typeid'] = '3060'
        paramDict['timeout'] = '60'
        paramDict['softid'] = '127153'
        paramDict['softkey'] = 'b82ac04048ed4087b0499896bea4b2d9'
        paramKeys = ['username',
                     'password',
                     'typeid',
                     'timeout',
                     'softid',
                     'softkey'
                     ]

        img = self.get_captcha_image(imagePath)
        if img is None:
            print 'get file error!'
            raise
        
        img.save(imagePath+"_upload.gif", format="gif")
        filebytes = open(imagePath+"_upload.gif", "rb").read()
        result = self.http_upload_image("http://api.ruokuai.com/create.xml", paramKeys, paramDict, filebytes)
        return self.get_captcha_value(result)
