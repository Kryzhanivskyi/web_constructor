import re
from io import BytesIO

import requests
import time
from PIL import Image
from django.conf import settings
from requests_html import HTMLSession
from django.core.management.base import BaseCommand, CommandError
from nodeads_libs.web_lib_core.models import DImageGroup, DImage


class Command(BaseCommand):
    help = 'Create random users'
    media_path = 'content/items/images'
    root_path = f'{settings.BASE_DIR}/media/{media_path}'

    def handle(self, *args, **kwargs):
        self.start()

    def start(self):
        gal_id_list, pic_gal_links = self.get_gal_id_list()
        
        for gal_index in range(0, len(gal_id_list), 1):
            gal_id = gal_id_list[gal_index]
            gal_name, pic_link_l_hd, pic_link_l_prev = self.get_pic_links_list(gal_id)
            group_id, group = self.create_group(gal_name, gal_index, pic_gal_links[gal_index])
            print('gal_name:', gal_name, ' gal_id:', group_id)
            for index in range(0, len(pic_link_l_hd), 1):
                pic_name = f'{group_id}_{index}'
                image = DImage()
                image.image_group = group
                image.is_visible = True
                image.order_index = int(index)
                image.url.name = self.create_image(pic_link_l_hd[index], pic_name)
                image.preview_url.name = self.create_image(pic_link_l_prev[index], pic_name+'_prev')
                image.save()
            print('created:', len(pic_link_l_hd), ' end.')
            time.sleep(1)

    def create_image(self, pic_link, pic_name):
        pic_path = f'{self.root_path}/{pic_name}.jpg'
        response = requests.get(pic_link, stream=True)
        img = Image.open(BytesIO(response.content))
        img = self.image_resize(img)
        img.save(pic_path)
        return f'{self.media_path}/{pic_name}.jpg'

    def image_resize(self, img):
        max_w_h = 1280
        width, height = img.size
        if width > max_w_h or height > max_w_h:
            if width > height:
                max_h = int((max_w_h * height) / width)
                img = img.resize((max_w_h, max_h), Image.ANTIALIAS)
            else:
                max_w = int((max_w_h * width) / height)
                img = img.resize((max_w, max_w_h), Image.ANTIALIAS)
        return img

    def create_group(self, gal_name, gal_index, pic_link):
        ''' доделать создание превью!'''
        group = DImageGroup()
        group.name = gal_name
        group.order_index = gal_index
        group.preview_url = self.create_image(pic_link, f'gal_{gal_index}_prev')
        group.save()
        return group.id, group

    def get_pic_links_list(self, gal_id):  # ['http://st0.vo.org.ua/images/0/124/41/p_493a968f29.jpg',]
        session = HTMLSession()
        r = session.get(f'http://vo.org.ua/gallery/{gal_id}')
        html_text = r.html.html
        gal_name = re.findall(r'<title id="title">(.*)<\/title>', html_text)[0]
        pic_link_l_prev = re.findall(r'(http:\/\/st0.vo.org.ua\/images\/\d+\/\d+\/\d+\/\w+.jpg)', html_text)
        pic_link_l_hd = list()
        for pic_link in pic_link_l_prev:
            pic_link_l_hd.append(pic_link.replace('/p_', '/f_'))
        return gal_name, pic_link_l_hd, pic_link_l_prev

    def get_gal_id_list(self):
        session = HTMLSession()
        r = session.get(f'http://vo.org.ua/gallery')
        html_text = r.html.html
        gal_id_list = re.findall(r'<a href="/gallery/(\d+)" ui-href="update" class="imageLoad">', html_text)
        pic_gal_links = re.findall(r'<img src="(http:\/\/st0.vo.org.ua\/images\/\d+\/\d+\/\d+\/\w+.jpg)"', html_text)
        return gal_id_list[::-1], pic_gal_links[::-1]

