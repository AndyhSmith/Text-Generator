import random
try:
    import requests 
except:
    print("Please install the requests module with 'pip install requests' in the terminal.")
    print("pip install requests")
    exit()
import json
import os

# ----------------- #
#   Menu Function   #
# ----------------- #

def menu():
    global selected_language
    clearTerminal()
    print("Used to generate non-sense text based on language patterns in Wikipedia articles.")
    print("-----------------")
    print("1. Choose Language: "+str(selected_language) + " (Current)")
    print("2. Generate Non-Sense Text")
    print("3. Train On More Data")
    print("4. Train On More Data (Random Language)")
    print("5. Exit")
    option = input("Option: ")
    if option == "1":
        chooseLanguage()
    elif option == "2":
        generate()      
    elif option == "3":
        train()
    elif option == "4":
        #todo
        pass
    elif option == "5":
        exit()
    elif option=="":
        clearTerminal()
        option=input("Are you sure you want to exit? (Y/N): ")
        if option.lower()=="y" or "":
            exit()
        
    menu()



# ----------------- #
#  Support Methods  #
# ----------------- #

# Load the data from a file
def loadJsonFromFile(file_path="./Languages/output.json"):
    with open(file_path, "r",errors="ignore",) as file: 
        file_content=file.read()
        if file_content == "":
            file_content="{}"
        return json.loads(file_content)

def createFile(file_path="./Languages/output.json"):
    with open(file_path, "w+") as file:
        file.write("{}")

# Convert the data to a string
def jsonToString():
    return json.dumps(data, indent=4)

# Save the content to a file
def saveToFile(file_path="output.json", content=""):
    with open(file_path, "w",encoding="utf-8") as file:
        file.write(content)

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def waitForUserInput():
    input("Press Enter to continue...")
# ----------------- #
# Core Methods      #
# ----------------- #




# Get a random article from Wikipedia
def downloadRandomWikiArticle():
    newArticle = False
    while not newArticle:
        # Get a random article from Wikipedia
        url = "https://"+languages[selected_language]+".wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json"
        # url = "https://es.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json"
        response = requests.get(url)
        pageData = json.loads(response.text)
        id=pageData["query"]["random"][0]["id"]
        title = pageData["query"]["random"][0]["title"]
        if id not in data["pages"]:
            newArticle = True
            data["pages"][id] = title
            print("New article:", title)

        # Get the content of the article
        url = "https://"+languages[selected_language]+".wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&format=json&titles=" + title
        response = requests.get(url)
        pageData = json.loads(response.text)
        content = pageData["query"]["pages"]
        page = list(content.keys())[0]
        content = content[page]["extract"]

    return str(content)




def parseOneSource():
    try:
        string = downloadRandomWikiArticle()
    except:
        return
    
    lastChar = ""
    for char in string:

        if lastChar == "":
            lastChar = char
            continue
        
        # If the lastChar is not in the data, add it
        if lastChar not in data:
            data[lastChar] = {}
            data[lastChar]["frequency"] = {}
            data[lastChar]["frequencyTotal"] = 0
            data[lastChar]["weights"] = {}

        # If the char is not in the data, add it
        if char not in data[lastChar]["frequency"]:
            data[lastChar]["frequency"][char] = 0
        
        data[lastChar]["frequency"][char] += 1
        data[lastChar]["frequencyTotal"] += 1
        
        lastChar = char



# Calculate the chance of each char
def calcChance():
    totalChars = 0
    for char in data:
        if "frequency" not in data[char]:
            continue
        for char2 in data[char]["frequency"]:
            data[char]["weights"][char2] = data[char]["frequency"][char2] / data[char]["frequencyTotal"]
        totalChars += data[char]["frequencyTotal"]
    
    data["firstCharWeight"] = {}
    for char in data:
        if "frequency" not in data[char]:
            continue
        data["firstCharWeight"][char] = data[char]["frequencyTotal"] / totalChars
    return totalChars



def saveTrainingData():
    totalChars=calcChance()
    data["stats"]["totalCharsAnalyzed"] = totalChars
    stringToSave = jsonToString()
    file_path="./Languages/"+str(selected_language.lower())+"_data"+".json"
    saveToFile(file_path,stringToSave)




def train():
    clearTerminal()
    if "totalCharsAnalyzed" not in data:
        data["stats"] = {}
        data["stats"]["totalCharsAnalyzed"] = 0
    if "pages" not in data:
        data["pages"] = {}

    previousCharCount = data["stats"]["totalCharsAnalyzed"]
    user_input=input("How many random Wikipedia article excerpts do you want to analyze? (Default: 5): ")
    if not user_input.isdigit():
        print("Invalid input, using default value of 5.")
        user_input=5

    for i in range(int(user_input)):
        print(i+1, "of", user_input,"- ", end="")
        parseOneSource()
        if i%3==0:
            saveTrainingData()
    

    saveTrainingData()
    newCharCount=data["stats"]["totalCharsAnalyzed"]-previousCharCount

    print("Complete")
    print("Total chars analyzed:",newCharCount)
    waitForUserInput()



# Generate a string
def generate():
    if len(data) == 0:
        print("No data for this language, please train first.")
        waitForUserInput()
        return
    print("Generating...")
    # Get a random char
    char = "a" # random.choice(list(data.keys()))
    char = random.choices(list(data["firstCharWeight"].keys()), list(data["firstCharWeight"].values()))[0]
    #char = random.choices(list(data.keys()), list(data["totalChance"].values()))[0]
    # print("First char:", str(random.choices(list(data.keys()), list(data.values()))))

    # Generate a string
    string = ""
    while True:
        # Get a random char based on the chance
        char = random.choices(list(data[char]["weights"].keys()), list(data[char]["weights"].values()))[0]
        string += char
        if char == ".":
            break
    print("String:", string)
    waitForUserInput()


def chooseLanguage():
    global selected_language
    clearTerminal()
    print("What language do you want to use?")
    user_input=input("Language: ")
    possible_languages=[]
    for language in languages:
        if user_input.lower() in language.lower():
            possible_languages.append(language)

    if len(possible_languages) > 1: 
        clearTerminal()     
        while True:
            print("Did you mean:")
            for i, language in enumerate(possible_languages):
                print(str(i+1)+".", language)
            user_input=input("Option: ")
            if user_input.isdigit() and int(user_input)-1 < len(possible_languages):
                selected_language=possible_languages[int(user_input)-1]
                break
        loadData()
    elif len(possible_languages) == 1:
        selected_language=possible_languages[0]
        loadData()
    else:
        print("No language found")
        waitForUserInput()

def loadData():
    global data
    data={}
    dataTemp=None
    file_path="./Languages/"+str(selected_language.lower())+"_data"+".json"
    try:
        data=loadJsonFromFile(file_path)
    except:
        print("File for language not found, creating new file.")
        createFile(file_path)
        loadData()


# ----------------- #
#       Main        #
# ----------------- #

clearTerminal()
# Global variables
data={}
selected_language="English"
loadData()


# Load the languages
languages=loadJsonFromFile("WikipediaWPCodes.json")


menu()