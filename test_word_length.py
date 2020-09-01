"""
Assert that the dynamic text (the lorem ipsum text block) on the page contains a word at least 10 characters in length.
Stretch goal:
Print the longest word on the page.
"""

# *** set up chromedriver path along with the page under test and time out value

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys


def test_setup():
    global driver
    chromedriver_path = '/usr/local/bin/chromedriver'
    timeout = 15  
    page_to_test = 'https://the-internet.herokuapp.com/dynamic_content'
    driver = webdriver.Chrome(chromedriver_path)
    driver.implicitly_wait(timeout)
    driver.get(page_to_test)


# ***Test to verify page contains a word at least 10 chars in length.
# ***Find the longest word on the page
# ***Reports results if the requirement is met, assert otherwise.
def test_wordlength():
    expected_row_count = 3  # looking at the current state of the page
    xpath_start = "//div[@class='row']"  # used to build a row-specific xpath
    xpath_end = "/div[@class='large-10 columns']"  
    required_length = 10  # length requirement
    find_longest = True  # strech goal 
    # find how many rows of text there are on the page
    actual_row_count = len(driver.find_elements_by_xpath("/" + xpath_end))
    print("Total rows available on the page under test = %d" % actual_row_count)

    if actual_row_count != expected_row_count:
        print("Expected rount count does not match the actual row count." + " Actual row count is %d. Check xpath." % actual_row_count)

    required_length_met = False  
    max_length = 0  
    if find_longest:
        longest_words = [] 
    for i in range(1, actual_row_count + 1):
        text_xpath = xpath_start + "[" + str(i) + "]" + xpath_end
        try:
            row_text = driver.find_element_by_xpath(text_xpath)
        except NoSuchElementException as e:
            print("NoSuchElementException .\n%s" % e)
            driver.quit()
            sys.exit(1)

        # check the contents of the row
        if row_text.is_displayed():
            print("Text in row %d is available." % i)
        else:
            print("Text in row %d is NOT available." % i)

        print("The text in row %d is:\n%s" % (i, row_text.text))

        # Parse the row and split into words to calculate the length
        words = row_text.text.split()
        for word in words:
            word_len = len(word)
            print("Word length as we parse text in row %d - %s = %d " % (i, word, word_len))  # Remove it later
            if word_len < required_length and find_longest:
                if word_len > max_length:
                    max_length = word_len
                    longest_words = [word]

                elif word_len == max_length:
                    longest_words.append(word)
            if word_len >= required_length:
                if not required_length_met:
                    required_length_met = True
                    i_req_met = i
                    word_req_met = word
                if find_longest:
                    if word_len > max_length:
                        max_length = word_len
                        longest_words = [word]
                    elif word_len == max_length:
                        longest_words.append(word)
                else:
                    max_length = word_len
                    break
        if required_length_met:
            if find_longest:
                continue
            else:
                break

    print('\nRESULTS\n====================')
    # report results of searching for the longest word(s)
    if find_longest:
        # Print the longest word(s) on the page and their length.
        print("The longest (%d characters) word(s) on the page:" % max_length)
        print(longest_words)

    # report results of finding a word of required length
    if required_length_met:
        print_text = "Minimum length req of %d char was met first time " + \
                     "at the word '%s' in text row %d."
        print(print_text % (required_length, word_req_met, i_req_met))
    else:
        # Assert that the dynamic text on the page contains a word of at least
        # required_length in length.
        assert required_length_met, "Minimum length of %d char is NOT found." \
                                     % required_length


def test_teardown():
    # close the Selenium driver
    driver.close()
    driver.quit()
