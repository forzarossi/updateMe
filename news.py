from bs4 import BeautifulSoup
from googlesearch import search
import urllib.request
import _thread
import schedule
import time

def searchFor(item):
    query = item + " footballwhispers"

    for j in search(query, tld="com", num=1, stop=1, pause=2):
        return j

def main():
    more = True

    print("\n\n\n==================================================================================")
    print("                           TRANSFER NEWS FINDER")

    while more:
        print("\n==================================================================================")

        query = input("\nWhat would you like to search for? Use \'top\' for hottest news! \n[Type a player or team name or \'exit\' to quit]\n> ")
        query.lower()

        if query == "":
            gatherTop()
        elif query == "exit":
            exit(0)
        elif query == 'top':
            gatherTop()
        elif query == 'live':
            mainT = _thread.start_new_thread(main(), "main")
            liveT = _thread.start_new_thread(liveUpdate(),"live")
        else:
            gather(query)

def gatherTop():
    gatherTopNews()
    gatherTopPlayers()

def gatherTopNews():
    url = "http://www.skysports.com/transfer-centre"  # add football whispers next
    unfiltered_text = urllib.request.urlopen(url)
    site = BeautifulSoup(unfiltered_text, "html.parser")

    topstories = []
    print("\n\n==================================================================================")
    print("                              TODAY'S TOP NEWS                                    \n")
    print("==================================================================================\n")

    for line in site.find_all("strong"):
        if(len(line.get_text().split()) > 2):
            topstories.append(line.get_text())

    for line in topstories:
        print(line)

    print("\n---------------------------------------------------------------------------------\n\n")

def gatherTopPlayers():
    url = "https://www.footballwhispers.com/"
    unfiltered_text = urllib.request.urlopen(url)
    site = BeautifulSoup(unfiltered_text, "html.parser")

    print("\n==================================================================================")
    print("                             TOP TRANSFERS                                        \n")
    print("==================================================================================\n")

    for line in site.find_all("a"):
        text = line.get_text()
        text = text.replace("arrow_forward"," ")

        if(len(text) > 0):
            if text[len(text)-1].isdigit():
                num = text[len(text)-3:]
                print(text[0:len(text)-3] + " " + num +"/5")

    print("\n------------------------------------------------------------------\n\n")

def gather(query):
    gatherNews(query)
    gatherBio(query)

def gatherNews(query):
    url = "http://www.skysports.com/transfer-centre"
    unfiltered_text = urllib.request.urlopen(url)
    site = BeautifulSoup(unfiltered_text, "html.parser")

    url = searchFor(query)
    name = url.replace("https://www.footballwhispers.com/", "")
    name = name.replace("players/", "")
    name = name.replace("teams/", "")
    query = name.replace("-", " ")

    print("\n\n\n==================================================================================")
    print("                             TOP " + query.upper() + " NEWS")
    print("\n==================================================================================\n")

    count = 0

    for line in site.find_all("p"):
        text = line.get_text().lower()
        text = text.strip()

        for word in query.split(" "):
            if word in text:
                count = count + 1
                text = text.replace('\'',"")
                text = text.title()

                print(text)

    if count == 0:
        print("There is no top news today on " + query.title() + "! \n")

def gatherBio(query):
    url = searchFor(query)
    name = url.replace("https://www.footballwhispers.com/", "")
    name = name.replace("players/","")
    name = name.replace("teams/","")
    name = name.replace("-", " ")
    name = name.title()

    if "players" in url:
        print("\n----------------------------------------------------------------------------------\n")
        print("                 -----SEARCHING FOR "+ name.upper() + "\'S BIO-----")
        print("\n----------------------------------------------------------------------------------\n")

        unfiltered_text = urllib.request.urlopen(url)
        site = BeautifulSoup(unfiltered_text, "html.parser")



        age = ""
        country = ""
        value = ""
        team = ""
        bio = ""

        for line in site.find_all("span"):
            text = line.get_text()
            if name + " is" in text:
                bio = text

        for line in site.find_all("a"):
            text = line.get_text()
            if "Team" in text:
                text = text.replace("keyboard_arrow_right", "")
                text = text.replace("Team", "")
                team = text

        for line in site.find_all("a"):
            text = line.get_text()
            if "Country" in text:
                text = text.replace("keyboard_arrow_right", "")
                text = text.replace("Country", "")
                country = text

        for line in site.find_all("div"):
            text = line.get_text()
            if "Age" in text:
                text = text.replace("keyboard_arrow_right", "")
                text = text.replace("Age", "")
                if len(text) > 0:
                    if text[0].isdigit():
                        age = text

        for line in site.find_all("div"):
            text = line.get_text()
            if "Value" in text:
                text = text.replace("keyboard_arrow_right", "")
                text = text.replace("Value", "")
                if len(text) > 0:
                    if text[0] == "£":
                        value = text

        print("Player Name: " + name + "                          Player's Age: " + age)
        print("Player's Country: " + country + "                             Player's value: " + value)
        print("Player Team: " + team + "\n\n")

        print(
            "----BIO---------------------------------------------------------------------------\n\n" + bio + "\nMore Here: " + url)
    gatherTransfer(url, name)

def gatherTransfer(url, name):
    unfiltered_text = urllib.request.urlopen(url)
    site = BeautifulSoup(unfiltered_text, "html.parser")

    print("\n==================================================================================")
    print(name.upper()+"'S POSSIBLE TRANSFER DESTINATIONS                          \n")
    print("==================================================================================")
    values = []

    for line in site.find_all():
        text = line.get_text()
        text = text.replace("arrow_forward", " ")
        text = text.replace("Forward"," ")
        text = text.replace("Midfielder", " ")
        text = text.replace("Goalkeeper", " ")
        text = text.replace("Defender", " ")

        if (len(text) > 0):
            if text[len(text) - 1].isdigit():
                num = text[len(text) - 3:]
                text = text[0:len(text) - 3]
                if((text,num) not in values ):
                    if("." in num):
                        values.append((text,num))

    for key in values:
        if(len(key[0]) > 4 and len(key[0])<30):
            if(float(key[1]) > 1):
                if key[0] != "shots" and key[0] != "aerial duels won" and "pass" not in key[0]:
                    print("To: " + key[0] +" " + key[1]+"/5\n")

def liveUpdate():
    getOriginal(gatherAndSave())
    schedule.every(5).minutes.do(getNew)

    while True:
        schedule.run_pending()
        time.sleep(1)

def gatherAndSave():
    url = "http://www.skysports.com/transfer-centre"
    unfiltered_text = urllib.request.urlopen(url)
    site = BeautifulSoup(unfiltered_text, "html.parser")

    return site.find_all("p")

def getOriginal(page):
    global _content
    _content = ""
    for line in page:
        filtered = line.get_text()
        filtered = filtered.replace("<p>","")
        filtered = filtered.replace("</p>","\n")
        filtered = filtered.replace("<strong>", "")
        filtered = filtered.replace("</strong>", "")

        if filtered not in _content:
            _content += filtered
    _content += "\n\n\n"

def getNew():
    global _content

    url = "http://www.skysports.com/transfer-centre"
    unfiltered_text = urllib.request.urlopen(url)
    site = BeautifulSoup(unfiltered_text, "html.parser")

    page = site.find_all("p")
    new = ""

    for line in page:
        filtered = line.get_text()
        filtered = filtered.replace("<p>","")
        filtered = filtered.replace("</p>","\n")
        filtered = filtered.replace("<strong>", "")
        filtered = filtered.replace("</strong>", "")

        if filtered not in _content:
            new += filtered

    if len(new.split()) > 1:
        print("\n==================================================================================")
        print("                                 NEW NEWS!\n")
        print("==================================================================================")

        dupesRemoved=""
        new = new.split("\n")
        for line in new:
            if line not in dupesRemoved:
                dupesRemoved += line + "\n"

        print(dupesRemoved)

        _content += "\n\n\n" + dupesRemoved

main()