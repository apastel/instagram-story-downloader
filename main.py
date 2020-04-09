from instaloader import Instaloader, Profile
import yaml
import os

L = Instaloader(dirname_pattern='data/{target}', save_metadata=False, download_video_thumbnails=False)
config = yaml.safe_load(open('config.yaml'))

if not os.path.exists('session'):
    os.mkdir('session')

for user in config['users']:
    try:
        L.load_session_from_file(user, f'session/{user}.session')
    except:
        L.interactive_login(user)
    
    L.save_session_to_file(f'session/{user}.session')

    # Download profiles at a time in case one of them has a problem, it doesn't crash the whole process
    for username in config['users'][user]['profiles']:
        print(f'\n=== {username} ===')
        try:
            profile = Profile.from_username(L.context, username)
            L.download_profiles([profile], profile_pic=False, posts=False, stories=True, fast_update=True)
        except Exception as e:
            print(e)

