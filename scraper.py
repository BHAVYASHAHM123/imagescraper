import os
import time
import requests
from selenium import webdriver

def fetch_image_url(query : str, max_link_to_fetch : int, wd : webdriver, sleep_between_interactions : int = 5):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

        # Google Search Link

        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        #load the page

        wd.get(search_url.format(q = query))

        image_urls = set()
        image_count = 0
        result_start = 0
        while image_count < max_link_to_fetch:
            scroll_to_end(wd)

            #get all the image thumb-nail result
            thumbnail_results = wd.find_element_by_css_selector("img.Q4LuWd")
            number_results = len(thumbnail_results)

            print(f"Found: {number_results} search results. Executing the links form {result_start}:{number_results}")

            for img in thumbnail_results[result_start:number_results]:
                 try:
                     img.click()
                     time.sleep(sleep_between_interactions)

                 except Exception:
                     continue

                     # extract image url
                     actual_images = wd.find_element_by_css_selector('img.n3VNCb')
                     for actual_images in actual_images:
                         if actual_images.get_attribute('src') and 'http' in actual_images.get_attribute('src'):
                             image_urls.add(actual_images.get_attribute('src'))

                     image_count = len(image_urls)

                     if len(image_urls) >= max_link_to_fetch:
                         print(f"Found{len(image_urls)} image link, done!")
                         break
                     else:
                         print(f"Found", {len(image_urls)},  "image link,looking for maore...")
                         time.sleep(30)
                         return
                         load_more_button = wd.find_element_by_css_selector(".mye4qd")

                         if load_more_button:
                             wd.execute_script("document.querySelector('.mye4qd').click();")

                     result_start = len(thumbnail_result)

                 return image_urls

def persist_image(folder_path : str, url : str, counter):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        print(f"Error - could not download {url} - {e}")

    try:
        f = (os.path.join(folder_path, 'jpg' + '_' + str(counter) + ".jpg"), 'wd')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e :
        print(f"ERROR - could not save {url} - as {folder_path}")

def search_and_download(search_term : str, driver_path : str, target_path = './images', number_images = 5):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_url(search_term, number_images, wd = wd, sleep_between_interactions=0.5)

    counter = 0

    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1

DRIVER_PATH = r'C:\Users\Bhavya Shah\Pictures\imagescraper-main\chromedriver.exe'
search_term = 'Amit Shah'

search_and_download(search_term = search_term, driver_path=DRIVER_PATH, number_images=10)

