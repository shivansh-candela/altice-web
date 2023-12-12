import time
import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import  Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.touch_actions import TouchActions

from matplotlib import pyplot as plt
import pandas as pd


datetime_format = "%H:%M:%S:%f"

chrome_options = Options()
chrome_options.add_argument('--use-fake-device-for-media-stream')
chrome_options.add_argument('--use-fake-ui-for-media-stream')
driver = webdriver.Chrome() #executable_path="/home/agent11/Desktop/chromedriver", options=chrome_options)
driver.maximize_window()
driver.get("https://developer.amazon.com/alexa/console/ask")
username = driver.find_element(By.ID, 'ap_email')
password = driver.find_element(By.ID, 'ap_password')
username.send_keys('itsvishwaksen@gmail.com')
password.send_keys('Lanforge@123')
password.submit()
time.sleep(10)
# while(True):
#     pass
skill_name = "skill-sample-python-smarthome-switch"
driver.find_element(By.LINK_TEXT, skill_name).click()
driver.find_element(By.CLASS_NAME, "astro-modal-dialog-close-icon").click()
driver.find_element(By.LINK_TEXT, "Test").click()
driver.find_element(By.ID, "deviceDisplay-label").click()
driver.find_element(By.ID, "alexa_smart_home_test-label").click()
driver.find_element(By.ID, "alexa_smart_home_debugger-label").click()
driver.find_element(By.ID, "skillLevel-label").click()
driver.find_element(By.ID, "deviceLevel-label").click()

commands = ['Turn on Light', 'Turn off Light']

for iter in range(5):

    test_results = {}

    for i in commands:
        test_results[i.lower()] = {
            'count': 0,
            'latencies': [],
            'success': 0,
            'fail': 0
        }

    command_one = driver.find_element(By.CLASS_NAME, "react-autosuggest__input")
    command_one.send_keys(commands[0])
    command_one.send_keys(Keys.ENTER)
    time.sleep(5)
    # driver.find_element(By.XPATH, "/html/body/div[1]/div/div/img[1]").click()
    event_start = driver.find_element(By.XPATH, "//*[@id='root']/div/div/section[2]/div[2]/div[2]/div[4]/div/div[1]/div/div[11]/span")
    command_two = driver.find_element(By.CLASS_NAME, "react-autosuggest__input")
    command_two.send_keys(commands[1])
    command_two.send_keys(Keys.ENTER)

    time.sleep(5)

    command_three = driver.find_element(By.CLASS_NAME, "react-autosuggest__input")
    command_three.send_keys(commands[2])
    command_three.send_keys(Keys.ENTER)
    time.sleep(5)

    get_requests = driver.find_elements(By.CLASS_NAME, "askt-dialog__message--request")
    alexa_chat_requests = []
    for req in get_requests:
        print(req)
        alexa_chat_requests.append(req.text)


    time.sleep(5)

    get_responses = driver.find_elements(By.CLASS_NAME, "askt-dialog__message--response")

    get_active_response = driver.find_element(By.CLASS_NAME, "askt-dialog__message--active-response")
    # print(get_active_response.text)
    alexa_chat_responses = []
    for res in get_responses:
        alexa_chat_responses.append(res.text)

    alexa_chat_responses.append(get_active_response.text)

    print(alexa_chat_requests)
    print(alexa_chat_responses)

    # while(True):
    #     pass

    for i in range(len(alexa_chat_requests)):
        print(alexa_chat_requests[i], '---------', alexa_chat_responses[i])

    time.sleep(5)
    get_result_cmd = driver.find_elements(By.CLASS_NAME, "askt-log__list-element")
    requests = []
    responses = []
    for packet in get_result_cmd:
        if('Event: Text.TextMessage' in packet.text):
            # requests.append(packet.text.split()[0][1:].strip(']'))
            packet.click()
            # print(driver.find_element(By.CLASS_NAME, "ace_scroller").get_attribute('innerText'))
            requests.append(datetime.strptime(packet.text.split()[0].strip('[').strip(']'), datetime_format))
        elif('Directive: SpeechRecognizer.RequestProcessingCompleted' in packet.text):
            responses.append(datetime.strptime(packet.text.split()[0].strip('[').strip(']'), datetime_format))

    print(len(requests) == len(responses))

    latency = []
    for i in range(len(requests)):
        latency.append((responses[i] - requests[i]).total_seconds() * 1000)

    # while(True):
    #     pass

    for i in range(len(requests)):
        # print(alexa_chat_requests[i], alexa_chat_responses[i], latency[i], sep='\t')
        current_request = alexa_chat_requests[i]
        current_response = alexa_chat_responses[i]

        test_results[current_request]['count'] += 1
        if('ok' in current_response):
            test_results[current_request]['success'] += 1
        else:
            test_results[current_request]['fail'] += 1
        
        test_results[current_request]['latencies'].append(latency[i])

print(test_results)


# generating graphs
commands = []
sent = []
passed = []
failed = []

for command, data in test_results.items():
    commands.append(command)
    sent.append(data['count'])
    passed.append(data['success'])
    failed.append(data['fail'])

# sent vs pass vs failed

# print({
#     'count': sent,
#     'success': passed,
#     'fail': failed
# })
# print(commands)

df = pd.DataFrame({
    'count': sent,
    'success': passed,
    'fail': failed
}, index=commands)

ax = df.plot.barh()
plt.savefig('Bulb on and off.png')

# device vs latencies
dataframes = []
for command, data in test_results.items():
    dataframes.append(pd.DataFrame(data= {
        command: data['latencies']
    }))

# Create matplotlib.axes object so df2 can share df1's axis
initial_df = dataframes[0]
initial_df = initial_df.plot()
for df in dataframes[1:]:
    df.plot(ax=initial_df)

plt.savefig('Bulb latencies.png')


# while(True):
#     pass
# driver.send_keys(Keys.PAGE_DOWN)
# event_end = driver.find_element_by_xpath("//*[@id='root']/div/div/section[2]/div[2]/div[2]/div[4]/div/div[1]/div/div[14]/span")
# print(event_end.text)

# driver.quit()
