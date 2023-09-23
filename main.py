print("Loading Speech Recognition...")
import speech_recognition as sr

print("Loading Text To Speech modules...")
import numpy
import torch 
from TTS.api import TTS 

from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import split_on_silence
import os
import json
import random

#Custom classes
from contextcontainers.wordcontextcontainer import WordContextContainer

from actions.lookup import LookUpAction
from actions.lookupv import LookUpVAction
from actions.lookupDate import LookUpDateAction
from actions.lookupDay import LookUpDayAction
from actions.print import PrintAction
from actions.referenceobject import ReferenceObjectAction
from actions.reference import ReferenceAction
from actions.writeVToSpeak import WriteVAction
from actions.writeTToSpeak import WriteTAction
from actions.writeToSpeak import WriteAction
from actions.say import SpeakAction
from actions.parsefactaction import ParseFactAction
from actions.addsubprocess import AddSubProcessAction
from actions.parsesegment import ParseSegmentAction
from actions.mathop import MathOpAction
from actions.goto import GotoAction
from actions.jumpiffalse import JIFAction
from actions.compareequals import CompareEqualsAction

from sprocesses.countdown import CountdownSubprocess
from sprocesses.timer import TimerSubprocess

from data.databall import DataBall

print("Loading dictionaries, libraries, and facts...")
dictionary = json.loads(open(os.path.join("dictionary.json"),"r").read())
library = json.loads(open(os.path.join("library.json"),"r").read())
facts = json.loads(open(os.path.join("facts.json"),"r").read())
contractions = json.loads(open(os.path.join("contractions.json"),"r").read())

object_memory = {}
object_facts = {}

subprocesses = []

for j in dictionary:
    x = {}
    x["name"] = dictionary[j]["text"]
    try:
        x["summary"] = dictionary[j]["summary"]
    except:
        None
    try:
        x["attributes"] = dictionary[j]["attributes"]
    except:
        x["attributes"] = {}
    try:
        x["tags"] = dictionary[j]["tags"]
    except:
        x["tags"] = {}

    if "number" in dictionary[j]:
        x["number"] = dictionary[j]["number"]
    object_memory[x["name"]] = x

for i in facts:
    x = object_memory[i]
    for j in facts[i]:
        x["attributes"][j] = {}
        for f in facts[i][j]:
            x["attributes"][j][f] = facts[i][j][f]


ACTIONS = []
ACTIONS.append(ReferenceObjectAction())
ACTIONS.append(ReferenceAction())
ACTIONS.append(LookUpAction())
ACTIONS.append(LookUpVAction())
ACTIONS.append(LookUpDateAction())
ACTIONS.append(LookUpDayAction())
ACTIONS.append(PrintAction())
ACTIONS.append(WriteAction())
ACTIONS.append(WriteVAction())
ACTIONS.append(WriteTAction())
ACTIONS.append(SpeakAction())
ACTIONS.append(ParseFactAction())
ACTIONS.append(AddSubProcessAction())
ACTIONS.append(ParseSegmentAction())
ACTIONS.append(MathOpAction())
ACTIONS.append(GotoAction())
ACTIONS.append(JIFAction())
ACTIONS.append(CompareEqualsAction())


SUBPROCESSES = []
SUBPROCESSES.append(CountdownSubprocess())
SUBPROCESSES.append(TimerSubprocess())

r = sr.Recognizer()
r.energy_threshold=270


def getVoice():
    with sr.Microphone() as source:
        text = ""
        try:
            temp = r.listen(source=source,timeout=0.7)
            try:
                text = r.recognize_google(temp)
            except:
                print("Unable to detect words.")
        except:
            return ""
    return text.lower()

def findRightMeaning(words, index):
    wordsEnd = words[index:]
    
    cc = WordContextContainer(wordsEnd)
    cc.process(dictionary,object_memory)

    return cc


        


def main():
    # Get device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    #print(TTS().list_models())

    # Init TTS
    tts = TTS("tts_models/en/ljspeech/tacotron2-DCA").to(device)
    #wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])

    print("***************************************************************************")
    print("Please note that the first word spoken normally does not get detected.")
    print("Try making a noise or say a test phrase first before saying what you want to say.")
    print("***************************************************************************")
    speak("HSR online",tts)

    #The core loop.
    while True:

        #Check subprocesses first. If the subprocess returns true ion the tick method, ther subprocess is complete.
        subprocessDataball = DataBall(ACTIONS=ACTIONS,memory=object_memory,SUBPROCESSES=SUBPROCESSES,subprocesses=subprocesses,speakmethod=speak,tts=tts, parsemethod=parseString, wordprocessingmethod=findRightMeaning)
        listToRemove = []
        for subprocess in subprocesses:
            if subprocess.tick(subprocessDataball):
                listToRemove.append(subprocess)

        for i in listToRemove:
            subprocesses.remove(i)



        #Get the spoken phrase
        text = getVoice()
        if(len(text)==0):
            continue
        
        #Strip punctuation
        text = text.replace("'","").replace(",","")

        #Replace contractions with the full words, for easier detection
        for c in contractions:
            if(text.startswith(contractions[c]["key"]+" ")):
                text = contractions[c]["value"]+text[len(contractions[c]["key"]):]
            if(text.endswith(" "+contractions[c]["key"])):
                text = text[:len(contractions[c]["key"])]+contractions[c]["value"]
            text = text.replace(" "+contractions[c]["key"]+" "," "+contractions[c]["value"]+" ")

        #Tokenize
        words = text.split(" ");    



        cc = []
        stack = []

        databall={}
        #Find the right meaning for each of the words
        for i in range(0,len(words)):
            meaning = findRightMeaning(words,i)
            cc.append(meaning)
            i=i+len(meaning.text)-1

        print("Translating \""+text+"\"")
        contextText = ""
        for i in cc:
            if len(contextText)==0:
                contextText = i.str()
            else:
                contextText = contextText+" "+i.str()
        print(contextText)
        

        #Check which sentence structures match the phrase provided
        listOfSentenceChecks = parseString(words=words,meaninglist=cc)
        

        if len(listOfSentenceChecks) == 0:
            print("No sentences matched :(")
            continue

        #Choose one of the sentence structures if there are multiple matching
        value = listOfSentenceChecks[random.randint(0,len(listOfSentenceChecks)-1)]
        selectedSentence = value["jj"]
        stack = []
        
        for action in selectedSentence["stack"]:
            stack.append(action)
        for k in value["databall"]:
            databall[k]=value["databall"][k]

        databall["deep"] = 1
                

        actiondataball = DataBall(ACTIONS=ACTIONS,memory=object_memory,speakmethod=speak,SUBPROCESSES=SUBPROCESSES,subprocesses=subprocesses,tts=tts,parsemethod=parseString, stack=stack, wordprocessingmethod = findRightMeaning, dictionary=dictionary)

        localactionindex = -1
        databall["actionindex"]=0
        while localactionindex != databall["actionindex"] or localactionindex==-1:
            localactionindex=0
            if(databall["actionindex"]>len(stack)):
                break
            for actionraw in stack:
                actionsplit = actionraw.split(":",1)
                actionname = actionsplit[0]
                parametersraw=actionsplit[1]
                params = []
                for i in range(0,parametersraw.count(":")+1):
                    split = parametersraw.split(":",1)
                    params.append(split[0])
                    if len(split)>1:
                        parametersraw=split[1]

                if localactionindex!=databall["actionindex"]:
                    localactionindex+=1
                    continue


                for a in ACTIONS:
                    if a.name == actionname:
                        a.setParameters(params)
                        a.action(databall,cc,actiondataball)
                databall["actionindex"]=databall["actionindex"]+1
                localactionindex+=1


def parseString(words, meaninglist):
        """Parses the words in the words parameter, and returns an dictionary where "jj" (Name will change) is equal to the command/sentence structure, while "databall" is equal to all the variables that need to be associated with that command/sentence"""
        listOfSentenceChecks = []
        highestListPriority = -2

        #If no words were provided for parsing, return early
        if(len(words)==0):
            return listOfSentenceChecks

        #Loop through all the sentence structures and commands
        for sentencekey in library:
            sentencestructuredata = library[sentencekey]
            isPattern = True
            inputindex = 0

            nonoptional_words = 0
            optional_words = 0

            tdataball = {}
            

            if(len(sentencestructuredata["input"]) > len(meaninglist)):
                continue

            #First determine how many optional words, non-optional words there are and whether there is a star operator
            for inputWords in sentencestructuredata["input"]:
                if inputWords.startswith("*") or inputWords.startswith("?*"):
                    nonoptional_words+=1

                elif not inputWords.startswith("?"):
                    nonoptional_words=nonoptional_words+1
                else:
                    optional_words=optional_words+1

            
            #Tag each section appropriately
            wordChunks = []
            for inputWordsIndex in range(0,len(sentencestructuredata["input"])):
                inputWords = sentencestructuredata["input"][inputWordsIndex]
                ball = {}
                #First detect the name of each section
                if inputWords.count(":")>0:
                    split = inputWords.split(":")
                    ball["name"] = split[1]
                    ball["index"] = inputindex
                    inputWords = split[0]

                #If the stasr operator is used
                if inputWords == "*":
                    ball["words"] = []
                    #if its at the end of the sentence structure
                    if(len(sentencestructuredata["input"]) <= inputindex+1):   
                        for appp in range(inputindex,len(meaninglist)):
                            ball["words"].append(meaninglist[appp]) 
                        wordChunks.append(ball)
                        continue

                    if len(meaninglist) > inputindex:                                    
                        ball["words"].append(meaninglist[inputindex]) 
                    loopbool = True
                    inputWordsIndex+=1
                    #if not, loop until it finds the next input word that ends this section
                    while loopbool:
                        inputindex+=1

                        if len(sentencestructuredata["input"]) <= inputWordsIndex:
                            if(len(meaninglist) > inputindex):
                                ball["words"].append(meaninglist[inputindex]) 
                            loopbool = False

                        else:
                            inputWords = sentencestructuredata["input"][inputWordsIndex]
                            if inputWords.count(":")>0:
                                split = inputWords.split(":")
                                inputWords = split[0]

                            if(inputWords == "*"):
                                if(len(meaninglist) > inputindex):
                                    ball["words"].append(meaninglist[inputindex]) 
                            else:
                                if len(meaninglist) <= inputindex:
                                    break
                                for m in meaninglist[inputindex].text:
                                    if(m == inputWords):
                                        loopbool = False
                                        break

                                for m in meaninglist[inputindex].tags:
                                    if("{"+m+"}" == inputWords):
                                        loopbool = False
                                        break
                                if(loopbool):
                                    ball["words"].append(meaninglist[inputindex]) 
                    wordChunks.append(ball)
                        

                else:
                    #Else, if no star operator is used, and its a regular check
                    foundword = False
                    if len(meaninglist) <= inputindex:
                        isPattern = False
                        continue
                    for m in meaninglist[inputindex].text:
                        if(m == inputWords):
                            foundword = True
                            break

                    for m in meaninglist[inputindex].tags:
                        if("{"+m+"}" == inputWords):
                            foundword = True
                            break
                        
                    #If the word was found, append the ball to wordchunks. If not found, set isPattern to false 
                    if(foundword):
                        ball["words"] = []
                        ball["words"].append(meaninglist[inputindex])    
                        inputindex+=1
                        wordChunks.append(ball)
                    else:
                        isPattern = False

            #Finally, this adds the data to the databall
            for t in wordChunks:
                if "name" in t:
                    stringname = t["name"]
                    tdataball["var_"+stringname] = t["index"]
                    tdataball["varlen_"+stringname] = len(t["words"])
                

            #If the pattern was found, add it to the list of sentences
            if isPattern:
                if inputindex <= len(meaninglist):
                    if sentencestructuredata["priority"] > highestListPriority:
                        highestListPriority = sentencestructuredata["priority"]
                        listOfSentenceChecks = []
                        listOfSentenceChecks.append({
                            "jj":sentencestructuredata,
                            "databall":tdataball
                            })
                    elif sentencestructuredata["priority"] == highestListPriority:
                        listOfSentenceChecks.append({
                            "jj":sentencestructuredata,
                            "databall":tdataball
                            })
        return listOfSentenceChecks



def speak(message, tts):
    """Prints out the message, and creates and plays an audio for the message."""
    if type(message) is not str:
        message = str(message)
    message=message.strip()
    print("HSR: "+message)
    #If the audio file does not exist, create it
    if not os.path.exists(os.path.join("voice",message+".wav")):
        count = 0
        for path in os.listdir(os.path.join("voice")):
            if os.path.isfile(os.path.join("voice",path)):
                count=count+1
        if count > 400:
            audiofile = None
            lastmodified = -1
            for path in os.listdir(os.path.join("voice")):
                if os.path.isfile(os.path.join("voice",path)):
                    if lastmodified == -1 or  os.path.getmtime(os.path.join("voice",path))< lastmodified:
                        lastmodified =  os.path.getmtime(os.path.join("voice",path))
                        audiofile = path

            print("Deleting oldest audio file: "+audiofile)
            os.remove(os.path.join("voice",audiofile))



        tts.tts_to_file(message+".", file_path="voice/"+message+".wav")
    init = AudioSegment.from_wav("voice/"+message+".wav")
    play(init)


main()