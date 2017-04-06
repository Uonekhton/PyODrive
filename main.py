# -*- coding: utf-8 -*-
import onedrivesdk, os, requests, argparse

redirect_uri = 'http://localhost:11462'
application_id = ''
client_secret = ''
api_base_url='https://api.onedrive.com/v1.0/'
scopes=['wl.signin', 'offline_access', 'onedrive.readwrite']
FILE_UPLOAD = './file.txt'
FILE_NAME = 'file.txt'
FOLDER_NAME = 'Python2'


class Main():
        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(
                http_provider, application_id, scopes)
        client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)

        def auth(auth_provider, client):
                try:
                        auth_provider.load_session()
                        auth_provider.refresh_token()
                except IOError:
                        auth_url = client.auth_provider.get_auth_url(redirect_uri)
                        print('Paste this URL into your browser, approve the app\'s access.')
                        print('Copy everything in the address bar after "code=", and paste it below.')
                        print(auth_url)
                        code = raw_input('Paste code here: ')
                        auth_provider.authenticate(code, redirect_uri, client_secret)
                        auth_provider.save_session()
                return client

        def get_sharing_link(client, return_file):
                global share
                permission = client.item(id=return_file.id).create_link("view").post()
                share = requests.get("{}".format(permission.link.web_url)).url.replace('redir', 'download')
                return share

        def get_deleting(name, auth_provider, client):
                collection = client.item(drive='me', id='root').children.request(top=100).get()
                for item in collection:
                        if item.name == name:
                                client.item(id=item.id).delete()
                                print u'Каталог удален'

        def get_upload(client, get_sharing_link):
                f = onedrivesdk.Folder()
                i = onedrivesdk.Item()
                i.name = FOLDER_NAME
                i.folder = f
                retur_folder = client.item(drive='me', id='root').children.add(i)
                try:
                        return_file = client.item(drive='me', id=retur_folder.id).children['%s' % FILE_NAME].upload(
                                FILE_UPLOAD)
                        get_sharing_link(client, return_file)
                        print share
                except IOError:
                        print u'Файл не найден'


        auth(auth_provider, client)
        #get_upload(client, get_sharing_link)
        get_deleting(FOLDER_NAME, auth_provider, client)
