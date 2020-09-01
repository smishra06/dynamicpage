"""
Assert that the "Punisher" image (silhouette with a skull on his chest) does not appear on the page.
This test may pass or fail on any given execution depending on whether the punisher happens to be on the page.
Stretch goal:
Give names to each avatar that can appear on the page and print out each avatars name.
"""
from selenium import webdriver
import json, os, shutil
import urllib.request


def test_setup():
    global driver
    chromedriver_path = '/usr/local/bin/chromedriver'
    timeout = 15  
    page_to_test = 'https://the-internet.herokuapp.com/dynamic_content'
    driver = webdriver.Chrome(chromedriver_path)
    driver.implicitly_wait(timeout)
    driver.get(page_to_test)


def test_punisher_present():
    expected_row_count = 3  # based on previous knowledge about the page layout
    xpath_avatars = "//div[@class='large-2 columns']/img"  # avatars' xpath
    name_p = 'Punisher'  # name of the avatar, which shouldn't be on the page
    url_p = 'https://the-internet.herokuapp.com/img/avatars/Original-' + \
            'Facebook-Geek-Profile-Avatar-3.jpg'  # URL of Punisher's image
    size_p = 12817  # size of Punisher's image
    punisher = {  # dictionary containing Punisher's attributes
        'name': name_p,
        'url': url_p,
        'size': size_p
    }
    # known_avatars is a list of dictionaries with attributes of known avatars
    if os.path.exists("known_avatars.json"):
        known_avatars = json.load(open("known_avatars.json"))
    else:
        known_avatars = [punisher]
    avatar_id = True 
    page_avatars = []  # Store avatar details
    punisher_absent = True  # Keep a check if punisher is present on the page

    # Get all avatars displayed on the page
    avatars = driver.find_elements_by_xpath(xpath_avatars)
    actual_row_count = len(avatars)  
    print("Total rows available on the page under test = %d" % actual_row_count)
    
    if actual_row_count != expected_row_count:
        print("Expected and actual row counts are different." + " Actual row count is %d. Check xpath." % actual_row_count)

    for n, avatar in enumerate(avatars, start=1):

        url = avatar.get_attribute('src')
        print("Avatar(row %d) URL is: %s" % (n, url))

        # save the avatar jpg file locally
        file_name = str(n) + 'av.jpg'
        print("Avatar(row %d) image downloaded as %s file" % (n, file_name))
        with urllib.request.urlopen(url) as resp, open(file_name, 'wb') as out_f:
            shutil.copyfileobj(resp, out_f)
        size = os.path.getsize(file_name)
        print("Avatar(row %d) file size is %d bytes" % (n, size))

        if avatar_id:
            url_m = False
            size_m = False
            known_av = []
            for known_av in known_avatars:
                if known_av['url'] == url:
                    url_m = True
                if known_av['size'] == size:
                    size_m = True
                if url_m or size_m:
                    break

            # If there is a match, check for Punisher.
            # Else give the avatar a name and add it to known avatars.
            # Add the avatar to the page's avatars
            if url_m and size_m:
                # check for Punisher
                if size == punisher['size']:
                    punisher_absent = False
                page_avatars.append(known_av)
            else:
                # Make avatar's name 'Avatar-[num]' by splicing its url
                name = url[-12:-4]
                new_av = {
                    'name': name,
                    'url': url,
                    'size': size
                }
                known_avatars.append(new_av)
                page_avatars.append(new_av)
                if url_m or size_m:
                    print('Only size or URL matches a known ' + 'avatar in row %d' % n)

                print(known_avatars)
        # If assigning names to avatars is not requested,
        # just check for Punisher
        else:
            if size == punisher['size'] and url == punisher['url']:
                punisher_absent = False
                break

    # Reporting results
    print('\nRESULTS\n====================')
    if avatar_id:
        # print out names of each avatar found on the page
        print("%d avatars found on the page:" % len(page_avatars))
        for av in page_avatars:
            print(av['name'])
        # Dump known_avatars as JSON file into working directory
        f = open("known_avatars.json", "w")
        json.dump(known_avatars, f)
        f.close()
    # Assert that Punisher image is not on the page
    if punisher_absent:
        assert print("Punisher was not found in the page.")


def test_teardown():
    driver.close()
    driver.quit()
