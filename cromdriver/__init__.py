from cromdriver.cromdriver import *

__version__ = '0.2.0'

latest_release_web = get_latest_release_web()
latest_release_file = get_latest_release_file()

print(latest_release_web, latest_release_file)
if latest_release_web == latest_release_file:
    print('OK')
    updating_path(get_release_directory(latest_release_file))

else:
    print('KO')
    create_release_directory(latest_release_web)

    url = get_chromedriver_url(latest_release_web)
    target_location = get_release_directory(latest_release_web)
    
    download_binary(url, target_location)
    set_latest_release_file(latest_release_web)
    latest_release_file = get_latest_release_file()

    updating_path(get_release_directory(latest_release_file))
    

