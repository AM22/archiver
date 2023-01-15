import difflib
import sys
import os
import math
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

SCROLL_PAUSE_TIME = 3

#get current timestamp as formatted string
def time_to_string():
    timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d_%H-%M-%S")

#scroll to the bottom to load all videos
def scroll_to_bottom(driver):
    #get number of videos
    num = int(driver.find_element_by_xpath('//*[@id="page-manager"]/ytd-browse/ytd-playlist-header-renderer/div/div[2]/div[1]/div/div[1]/div[1]/ytd-playlist-byline-renderer/div/yt-formatted-string[1]/span[1]').text)

    #calculate number of times to go to end
    times = math.ceil(num / 100)
    
    #scroll appropriate amount of times
    while times > 0:
        driver.find_element_by_tag_name('html').send_keys(Keys.END)
        time.sleep(SCROLL_PAUSE_TIME)
        times -= 1

if __name__ == "__main__":
    #perform validation checks on args
    args = sys.argv
    playlist_link = args[1]
    if "youtube.com" not in playlist_link:
        print("Not a valid YouTube playlist!")
        exit()
    
    if len(args) > 4:
        print("Too many arguments")
        exit()

    diff_name = "diff"
    if len(args) > 2 and args[2]:
        diff_name += time_to_string()

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(playlist_link)
    driver.implicitly_wait(5)
    
    scroll_to_bottom(driver)
    
    playlist = driver.find_element_by_xpath('//*[@id="contents"]')
    video_names = [vid.text for vid in playlist.find_elements_by_id('video-title')]

    playlist_name = driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-playlist-header-renderer/div/div[2]/div[1]/div/yt-dynamic-sizing-formatted-string/div/yt-formatted-string').text
    
    old_str = ""
    new_str = ""
    old_list = []
    #if playlist folder already exists, read in old playlist to compare to current playlist
    if os.path.isdir(playlist_name):
        old = open(os.path.join(playlist_name, 'titles.txt'), 'r', encoding='utf-8')
        for line in old:
            old_str += line
            old_list.append(line)
        old.close()
    #otherwise, create the folder
    else:
        os.mkdir(playlist_name)

    for name in video_names:
        new_str += name + '\n'

    #write the playlist to the output file
    new = open(os.path.join(playlist_name, 'titles.txt'), 'wb')
    new.write(new_str.encode('utf8'))
    new.close()

    #write the difference between the old playlist and the updated playlist 
    diff = open(os.path.join(playlist_name, diff_name + '.txt'), 'wb')

    # if set mode, write old songs that are missing from the new set of songs
    if len(args) == 4 and args[3]:
        new_set = set(video_names)
        print(new_set)
        for line in old_list:
            line = line[:-1]
            print(line)
            if line not in new_set:
                diff.write((line + '\n').encode('utf8'))
    else:
        for line in difflib.unified_diff(old_str.splitlines(), new_str.splitlines(), fromfile='old playlist names', tofile='new playlist names', lineterm=''):
            diff.write((line + '\n').encode('utf8'))
    diff.close()

    driver.quit()