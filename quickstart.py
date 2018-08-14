import os
import time
from tempfile import gettempdir

from selenium.common.exceptions import NoSuchElementException

from instapy import InstaPy

import userCredentials
insta_username = userCredentials.USERNAME
insta_password = userCredentials.PASSWORD

# headless_browser=True # set if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'

session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=False,
                  multi_logs=True)

try:
    session.login()

    # settings
    session.set_relationship_bounds(enabled=True,
				 potency_ratio=False,
				  delimit_by_numbers=True,
				   max_followers=459000000000,
				    max_following=5555000000000,
				     min_followers=45,
				      min_following=77)
    session.set_do_comment(True, percentage=10)
    session.set_comments(['aMEIzing!', 'So much fun!!', 'Nicey!'])
    session.set_dont_include(['friend1', 'friend2', 'friend3'])

    session.set_do_like(enabled=True, percentage=100)
    # session.set_dont_like(['pizza', 'girl'])

    # actions
    usersToFindFollowers = ["usernames_to_follow"]
    numFollowersToFind = 1
    session.logger.info("Finding {} followers of each user in list {}".format(numFollowersToFind, usersToFindFollowers))
    session.follow_user_followers(usersToFindFollowers, amount = numFollowersToFind, randomize=False)

    amountOfPicturesToLike = 2
    session.logger.info("Liking {} pictures of each follower in list: {}".format(amountOfPicturesToLike,
        session.person_list_to_like_posts))

    # session.like_by_users(session.person_list_to_like_posts, amount=amountOfPicturesToLike)

    # session.like_by_tags(['natgeo'], amount=1)

except Exception as exc:
    # if changes to IG layout, upload the file to help us locate the change
    if isinstance(exc, NoSuchElementException):
        file_path = os.path.join(gettempdir(), '{}.html'.format(time.strftime('%Y%m%d-%H%M%S')))
        with open(file_path, 'wb') as fp:
            fp.write(session.browser.page_source.encode('utf8'))
        print('{0}\nIf raising an issue, please also upload the file located at:\n{1}\n{0}'.format(
            '*' * 70, file_path))
    # full stacktrace when raising Github issue
    raise

finally:
    # end the bot session
    session.end()
