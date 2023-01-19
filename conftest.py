import pytest
import selenium.webdriver.firefox.options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox import firefox_profile
import uuid

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='en',
                     help="Choose language: 'ru' or 'en' or 'es' or 'fr'")

@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser_name")
    user_language = request.config.getoption("--language")

    browser = None
    if browser_name == "chrome":
        print("\nstart chrome browser for test..")
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        options.add_argument("-foreground") #-headless для скрытого режима
        # options.add_argument('--kiosk')
        browser = webdriver.Chrome(options=options)
        browser.set_window_size(1910, 1020)
        browser.implicitly_wait(15)
    elif browser_name == "firefox":
        print("\nstart firefox browser for test..")
        firefox_options = selenium.webdriver.firefox.options.Options()
        # firefox_options.set_preference("intl.accept_languages", user_language)
        firefox_options.add_argument("-foreground") #-headless для скрытого режима
        # firefox_options.add_argument("--kiosk")
        # browser = webdriver.Firefox(options=firefox_options)
        fp = webdriver.FirefoxProfile()
        fp.set_preference("intl.accept_languages", user_language)
        browser = webdriver.Firefox(firefox_profile=fp, options=firefox_options)
        print(f"Title: {browser.title}")
        browser.set_window_size(1910, 1020)
        browser.implicitly_wait(15)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass # just ignore any errors here
    print("\nquit browser..")
    browser.quit()