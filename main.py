from instaloader import Instaloader, Profile
import datetime
import yaml
import os

L = Instaloader(dirname_pattern='data/{target}', save_metadata=False, download_video_thumbnails=False)
config = yaml.safe_load(open('config.yaml'))

if not os.path.exists('session'):
    os.mkdir('session')

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
            last_24hrs = lambda post: post.date_utc >= datetime.datetime.today() - datetime.timedelta(days=1)
            L.download_profiles(
                [profile],
                profile_pic=False,
                posts=True,
                post_filter=last_24hrs,
                stories=True,
                fast_update=True
            )
        except Exception as e:
            print(e)
