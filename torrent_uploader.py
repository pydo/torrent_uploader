import requests
import shutil
import argparse

def seedpeer(args):
    """
    WORKING.

    First request GETS the captcha.
       2nd request POSTS using the cookie from captcha request.

       The request is a multipart encoded file.
       The file is opened in the file dict and has its content-type declared explicitly.

       The payload (data) includes most of the categories that need to be declared in the post request
       including the captcha from the original get request.
    """
    get_captcha = requests.get('http://www.seedpeer.eu/captcha.gif', stream=True)
    if get_captcha.status_code == 200:
        with open('captcha.gif', 'wb') as f:
            get_captcha.raw.decode_content = True
            shutil.copyfileobj(get_captcha.raw, f)
    captcha = input('Enter captcha:\n')
    files = {'file': (args.torrent, open(args.torrent, 'rb'),
                      'application/octet-stream')}
    payload = {'secure': captcha,
               'submit': 'Upload Torrent',
               'category': '18',
               'filename': args.torrent_name,
               'description': args.torrent_description}
    cookies = {'PHPSESSID': get_captcha.cookies['PHPSESSID']}
    upload_torrent = requests.post('http://www.seedpeer.eu/upload.html', files=files, data=payload, cookies=cookies)
    print(upload_torrent.status_code)
    print(upload_torrent.text)
    if 'AddThis Bookmark Button' in upload_torrent.text:
        print('Torrent uploaded successfully')
    elif 'This torrent exists' in upload_torrent.text:
        print('Torrent already exists')
    else:
        print('Torrent upload failed')


def parse_args():
    parser = argparse.ArgumentParser(description='Upload a torrent to seedpeer.eu')
    parser.add_argument("-t", "--torrent", action="store",
                        help="specify torrent file to upload", required=True)
    parser.add_argument('-tn', '--torrent_name', action='store',
                        help='specify a name for the torrent', required=True)
    parser.add_argument('-d', '--torrent_description', action='store',
                        help='specify a description for the torrent', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    seedpeer(parse_args())
