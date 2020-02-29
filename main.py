from instaloader import Instaloader, Profile
import yaml

L = Instaloader(dirname_pattern='data/{target}', save_metadata=False, download_video_thumbnails=False)
config = yaml.safe_load(open('config.yaml'))

for user in config['users']:
    try:
        L.load_session_from_file(user, f'data/{user}.session')
    except:
        L.interactive_login(user)
    
    L.save_session_to_file(f'data/{user}.session')

    profiles = [Profile.from_username(L.context, username) for username in config['users'][user]['profiles']]
    L.download_profiles(profiles, profile_pic=False, posts=False, stories=True, fast_update=True)
