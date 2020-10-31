import platform
import sys
import distro

LOGIN_URL = 'https://www.udemy.com/join/login-popup/?ref=&display_type=popup&loc'
LOGOUT_URL = 'http://www.udemy.com/user/logout'
COURSE_TITLE_URL = 'https://www.udemy.com/api-2.0/courses/{course_id}?fields[course]=title'
COURSE_INFO_URL = 'https://www.udemy.com/api-2.0/courses/{course_id}/cached-subscriber-curriculum-items?fields[asset]=@min,title,filename,asset_type,external_url,length&fields[chapter]=@min,description,object_index,title,sort_order&fields[lecture]=@min,object_index,asset,supplementary_assets,sort_order,is_published,is_free&fields[quiz]=@min,object_index,title,sort_order,is_published&page_size=550'
GET_LECTURE_URL = 'https://www.udemy.com/api-2.0/users/me/subscribed-courses/{course_id}/lectures/{lecture_id}?fields[lecture]=asset,description,download_url&fields[asset]=asset_type,stream_urls,thumbnail_url,download_urls'
ATTACHMENT_URL = 'https://www.udemy.com/api-2.0/users/me/subscribed-courses/{course_id}/lectures/{lecture_id}/supplementary-assets/{attachment_id}?fields[asset]=download_urls'


def sys_info():
    result = {
        'platform': '{} [{}]'.format(platform.platform(), platform.version()),
        'python': '{} {}'.format(
            platform.python_implementation(),
            sys.version.replace('\n', '')
        ),
        'os': 'Unknown'
    }

    linux_ver = distro.linux_distribution()
    mac_ver = platform.mac_ver()
    win_ver = platform.win32_ver()

    if linux_ver[0]:
        result['os'] = 'Linux - {}'.format(' '.join(linux_ver))
    elif mac_ver[0]:
        result['os'] = 'OS X - {}'.format(' '.join(mac_ver[::2]))
    elif win_ver[0]:
        result['os'] = 'Windows - {}'.format(' '.join(win_ver[:2]))

    return result

def unescape(string):
    """Replace some characters to nothing"""
    string = string.replace('/', '')
    string = string.replace('->', '')
    string = string.replace('(', '')
    string = string.replace(')', '')
    return string
