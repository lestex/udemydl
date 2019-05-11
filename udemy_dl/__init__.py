import logging

LOGIN_URL = 'https://www.udemy.com/join/login-popup/?displayType=ajax&display_type=popup&showSkipButton=1&returnUrlAfterLogin=https%3A%2F%2Fwww.udemy.com%2F&next=https%3A%2F%2Fwww.udemy.com%2F&locale=en_US'
LOGIN_POPUP_URL = 'https://www.udemy.com/join/login-popup'
LOGOUT_URL = 'http://www.udemy.com/user/logout'
COURSE_TITLE_URL = 'https://www.udemy.com/api-2.0/courses/{course_id}?fields[course]=title'
COURSE_INFO_URL = 'https://www.udemy.com/api-2.0/courses/{course_id}/cached-subscriber-curriculum-items?fields[asset]=@min,title,filename,asset_type,external_url,length&fields[chapter]=@min,description,object_index,title,sort_order&fields[lecture]=@min,object_index,asset,supplementary_assets,sort_order,is_published,is_free&fields[quiz]=@min,object_index,title,sort_order,is_published&page_size=550'
GET_LECTURE_URL = 'https://www.udemy.com/api-2.0/users/me/subscribed-courses/{course_id}/lectures/{lecture_id}?fields[lecture]=asset,description,download_url&fields[asset]=asset_type,stream_urls,thumbnail_url,download_urls'
ATTACHMENT_URL = 'https://www.udemy.com/api-2.0/users/me/subscribed-courses/{course_id}/lectures/{lecture_id}/supplementary-assets/{attachment_id}?fields[asset]=download_urls'

__title__ = 'udemydl'
__author__ = 'Andrey Larin'
__email__ = 'lestex@gmail.com'
__version__ = '0.5.0'

logger = logging.getLogger(__title__)
