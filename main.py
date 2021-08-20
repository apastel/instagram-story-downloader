from instaloader import Instaloader, Profile
# import datetime
import time
import yaml
import os

L = Instaloader(dirname_pattern='data/{target}', save_metadata=False, download_video_thumbnails=False)
config = yaml.safe_load(open('config.yaml'))

if not os.path.exists('session'):
    os.mkdir('session')

if not os.path.exists('data'):
    os.mkdir('data')

for account in config['accounts']:
    try:
        L.load_session_from_file(account, f'session/{account}.session')
    except:
        L.interactive_login(account)
    
    L.save_session_to_file(f'session/{account}.session')

    # Download profiles one at a time in case one of them has a problem, it doesn't crash the whole process
    for user in config['accounts'][account]:
        print(f"\n=== {user['profile']} ===")
        try:
            profile = Profile.from_username(L.context, user['profile'])
            # last_24hrs = lambda post: post.date_utc >= datetime.datetime.today() - datetime.timedelta(days=1)
            dl_posts = user['posts'] if 'posts' in user else True # download all posts unless otherwise specified
            dl_stories = user['stories'] if 'stories' in user else True # download all stories unless otherwise specified
            L.download_profiles(
                [profile],
                profile_pic=False,
                posts=dl_posts,
                # post_filter=last_24hrs,
                stories=dl_stories,
                fast_update=True
            )
        except Exception as e:
            print(e)
    
    time.sleep(10)
