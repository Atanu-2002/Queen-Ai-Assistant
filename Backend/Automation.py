from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
from AppOpener import open as appopen, give_appnames

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", 
           "LWkfke", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask."
]

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello,I am{os.environ['Username']}, You're a content writer.You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": Answer}) 
        return Answer
    
    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYouTube(query):
    playonyt(query)
    return True



USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

def OpenApp(app, sess=requests.session()):
    try:
        # Check if the app is installed
        available_apps = give_appnames()
        
        if app.lower() in [a.lower() for a in available_apps]:  
            appopen(app, match_closest=True, output=True, throw_error=True)
            print(f"Opened {app} on your PC.")
            return True
        else:
            print(f"{app} is not installed. Searching for the official website...")

    except Exception as e:
        print(f"Error opening {app} with AppOpener: {e}")

    # Function to search Google for the official website
    def search_bing(query):
        url = f"https://www.bing.com/search?q={query}+official+site"
        headers = {"User-Agent": USER_AGENT}
        try:
            response = sess.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
                return None
        except requests.exceptions.RequestException as err:
            print(f"Request failed: {err}")
            return None

    # Function to extract the first official website link
    def extract_links(html):
        if html is None:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            if "http" in href and "google" not in href:
                return href  # Return the first valid link
        return None

    # Search for the app's official website
    html = search_bing(app)

    if html:
        link = extract_links(html)
        if link:
            webbrowser.open(link)
            print(f"Opening {app}'s official website: {link}")
            return True
        else:
            print(f"No official website found for {app}.")
            return False
    else:
        print(f"Search failed for {app}.")
        return False



def CloseApp(app):

    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False
            

def System(command):

    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume unmute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True

async def TranslateAndExecute(commands: list[str]):

    funcs = []

    for command in commands:

        if command.startswith("open "):

            if "open it" in command:
                pass

            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)  

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)   

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)  

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)     

        else:
            print(f"No Function Found. For {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands):
        pass

    return True

if __name__ == "__main__":
    asyncio.run(Automation(["open facebook","open instagram","play victory anthem","content song for me"]))
                