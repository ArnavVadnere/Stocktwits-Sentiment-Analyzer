import json
import datetime
from selenium import webdriver
from textblob import TextBlob
import datetime
import time


def get_ticker():

    #gets symbol from user
    g = input("Please Enter Ticker Symbol: ")
    return g
def get_numdays():
    #gets symbol from user
    g = input("Please Enter Limit For Comments(in days): ")
    return g

if __name__ == "__main__":
    #declare variables
    json_sentiment = {}
    json_comment = {}
    Bullish = 0
    Bearish = 0
    totalcounter = 0
    #calls get_ticker function and creates stocktwits web address for that symbol
    ticker = get_ticker()
    website = ('https://stocktwits.com/symbol/' + str(ticker))
    numdays = get_numdays()
    #selenium requires webdrivers to perform in certain browers. In this case we are using FireFox and the webdriver
    #needed for this is geodriver.exe
    #the driver variable is set as the firefox webdriver .exe program
    #driver = webdriver.Firefox(executable_path=r'C:\Users\Arnav.Vadnere88\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe')
    driver = webdriver.Chrome(executable_path=r'C:\webdriver\chromedriver.exe')
    #FireFox webdriver then open up the website that we declared in line 23
    driver.get(website)

    #scroll down to allow more comments to be scrapped

    
    comment = {}
    todaytemp = datetime.datetime.now()
    today = datetime.date(int(todaytemp.year), int(todaytemp.month), int(todaytemp.day))
    max_time = today - datetime.timedelta(days = int(numdays))
    print('Max Date: ' + str(max_time))
    p = 0
    loop = True
    yes = 0
    start = 100
    '''
    end = time.time() + 40
    while time.time() < end:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(.24)
    print('done')
    
    '''
    while loop == True:
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        Divs = driver.find_elements_by_class_name('st_28bQfzV')

        

        #while ting == True:

        #for i in range(1)  :
        print('p', str(p))
        print('len divs', str(len(Divs)))
        if len(Divs) < 10:
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            ok = Divs[p].text
            p += 5
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.2)


            num = (len(Divs)) - p
            p += num - 10

        ok = Divs[p].text

        if 'm' in ok:
            continue
        elif 'now' in ok:
            continue
        elif '/' in ok:

            old_date = (ok)
            new_date = old_date.split('/')
            tempdate = new_date[2]
            tempdate = tempdate.split(' ')
            tempdate[0] = tempdate[0].replace(',', '')
            month = new_date[0]
            day = new_date[1]
            year = tempdate[0]
            year = '20' + year
            timenow = datetime.date(int(year), int(month), int(day))
            test = timenow <= max_time
            print('IN ELSE ', timenow)
            print(test)
        
            if test == True:
                print('BREAK', timenow)
                #print('MaxTime', max_time)
                
                loop = False
                ting = False
            else:
                loop = True
            ok = ''
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        Divs.clear()
        comment.clear()
  
    #'''
    print('loop ENDED')

    #uses html class name to find all comments and sentiments
    el = driver.find_elements_by_class_name('st_3SL2gug')
    le = driver.find_elements_by_class_name('st_11GoBZI')

    #finds number of comment and sentiments extracted
    length_el = len(el)
    length_le = len(le)

    #converts webelement list to regular list for easy access of data
    for i in range(length_el):
        comment[i] = el[i].text
    for i in range(length_le):
        json_sentiment[i] = le[i].text


    #adds comments that are Bullish or Bearish into corresponding counters
    for i in json_sentiment:
        if ((json_sentiment[i])) == 'Bearish':
            json_sentiment[i] = 'Bearish'
            Bearish += 1
            totalcounter += 1
        elif ((json_sentiment[i])) == ('Bullish'):
            json_sentiment[i] = 'Bullish'
            Bullish += 1
            totalcounter += 1
    total = Bearish + Bullish


    polarityShift = 0
    negative_keywords = ['loss','losing','low','hit','tumble','fell','fall','hurt','recession','worse', 'tanks', 'dives', 'skids', 'bearish', 'down', 'tests positive']
    positive_keywords = ['earn','gain','high','great','diversification','well', 'soars', 'pops', 'jumps', 'rallies', 'recovers', 'surges', 'bullish', 'up', 'tests negative']


    total_sentiment = {}
    sentance_polarity = {}

    for i in comment:
        blob = TextBlob(comment[i])
        for sentence in blob.sentences:
            polarityShift = 0
            
            for word in negative_keywords:
                if sentence.find(word.lower())!= -1:
                    polarityShift-=.25
                    
            for word in negative_keywords:
                if sentence.find(word)!= -1:
                    polarityShift-=.25
                    
            total_sentiment[i] = polarityShift
            sentance_polarity[i] = sentence.sentiment.polarity
        #print(comment[i])
        print(sentence.sentiment.polarity + polarityShift)

    #prints percentage of Bullish or Bearish comments           
    print('Percent Bullish')
    print((Bullish/total)*100)
    print('\nPercent Bearish')
    print((Bearish/total)*100)
    print('Total Counter(Flairs): ' + str(totalcounter))
    print(totalcounter)
    totalcounter = 0

    for i in total_sentiment:
        totalcounter += (total_sentiment[i] + sentance_polarity[i])

    avg_sentiment = (totalcounter)/(len(total_sentiment))
    print('Overall sentiment using NLP for ' + str(ticker) + ': ' + str(avg_sentiment))
    print('Total Counter(Comments): ' + len(comment))
    #driver.close()
