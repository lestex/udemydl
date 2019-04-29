import platform
import sys

def sys_info():
    result = {
        'platform': '{} [{}]'.format(platform.platform(), platform.version()),
        'python': '{} {}'.format(
            platform.python_implementation(),
            sys.version.replace('\n', '')
        ),
        'os': 'Unknown'
    }

    linux_ver = platform.linux_distribution()
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
