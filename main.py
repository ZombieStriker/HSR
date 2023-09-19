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


SUBPROCESSES = []
SUBPROCESSES.append(CountdownSubprocess())
SUBPROCESSES.append(TimerSubprocess())



def getVoice():
    with sr.Microphone() as source:
        r = sr.Recognizer()
        r.energy_threshold=350
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

    speak("HSR online",tts)
    while True:

        subprocessDataball = DataBall(ACTIONS=ACTIONS,memory=object_memory,SUBPROCESSES=SUBPROCESSES,subprocesses=subprocesses,speakmethod=speak,tts=tts)
        listToRemove = []
        for subprocess in subprocesses:
            if subprocess.tick(subprocessDataball):
                listToRemove.append(subprocess)

        for i in listToRemove:
            subprocesses.remove(i)




        text = getVoice()
        if(len(text)==0):
            continue
        
        #Strip punctuation
        text = text.replace("'","").replace(",","")

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
        lastjj = None

        databall={}

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
        

        listOfSentenceChecks = []
        highestListPriority = -2


        for j in library:
            jj = library[j]
            isPattern = True
            index = 0

            foundwords = 0
            nonoptional_words = 0
            optional_words = 0

            starOperator = False
            hasStarOperator = False
            tdataball = {}

            for inputWords in jj["input"]:
                if inputWords.startswith("*") or inputWords.startswith("?*"):
                    hasStarOperator = True

                elif not inputWords.startswith("?"):
                    nonoptional_words=nonoptional_words+1
                else:
                    optional_words=optional_words+1
            
            for inputWords in jj["input"]:
                    
                if(inputWords.count(":")>0):
                    inputsplit = inputWords.split(":")
                    inputWords=inputsplit[0]
                    tdataball["var_"+inputsplit[1]] = index

                if inputWords == "*":
                    starOperator=True
                    if(inputWords.count(":")>0):
                        inputsplit = inputWords.split(":")
                        inputWords=inputsplit[0]
                        tdataball["var_"+inputsplit[1]] = index
                    lenthOfVar = 1       
                    index=index+1
                    continue

                if starOperator:                     
                    while starOperator:        
                        isQuestionable = False
                        if len(cc) <= index:
                            break
                        meanings=cc[index]
                        if  inputWords.startswith("?"):
                            inputWords = inputWords[1:]
                            isQuestionable = True

                        tagfound = False
                        if not tagfound:
                            for name in meanings.text:
                                if inputWords == name:
                                    tagfound=True
                                    starOperator=False

                        if not tagfound:
                            for tags in meanings.tags:
                                if inputWords == "{"+tags+"}":
                                    tagfound=True
                                    starOperator = False
                                    break

                        if tagfound:
                            index=index+1  
                        else:
                            lenthOfVar=lenthOfVar+1  
                        
                    tdataball["varlen_"+inputsplit[1]] = lenthOfVar
                else:
                    isQuestionable = False
                    if len(cc) <= index:
                        continue
                    meanings=cc[index]

                    if not inputWords.startswith("?"):
                        index=index+1
                    else:
                        inputWords = inputWords[1:]
                        isQuestionable = True
                    tagfound = False
                    if inputWords == "*":
                        tagfound=True

                    if not tagfound:
                        for name in meanings.text:
                            if inputWords == name:
                                tagfound=True

                    if not tagfound:
                        for tags in meanings.tags:
                            if inputWords == "{"+tags+"}":
                                tagfound=True
                                break

                    if isQuestionable:
                        if tagfound:
                             index=index+1
                             foundwords=foundwords+1
                    elif not tagfound:
                        isPattern=False
                        continue
                    else:
                        foundwords=foundwords+1

            if starOperator:
                starOperator=False
                lenthOfVar=len(words)+1-index
                index = len(cc)
                tdataball["varlen_"+inputsplit[1]] = lenthOfVar

            
            if not hasStarOperator:
                if not (foundwords>= nonoptional_words and ((foundwords <= nonoptional_words+optional_words))):
                    #print("Not same length: "+str(foundwords)+" ["+str(nonoptional_words)+", "+str(nonoptional_words+optional_words)+"]")
                    continue


            if isPattern:
                if index == len(cc):
                    if jj["priority"] > highestListPriority:
                        highestListPriority = jj["priority"]
                        listOfSentenceChecks = []
                        listOfSentenceChecks.append({
                            "jj":jj,
                            "databall":tdataball
                            })
                    elif jj["priority"] == highestListPriority:
                        listOfSentenceChecks.append({
                            "jj":jj,
                            "databall":tdataball
                            })


        if len(listOfSentenceChecks) == 0:
            continue
        value = listOfSentenceChecks[random.randint(0,len(listOfSentenceChecks)-1)]
        selectedSentence = value["jj"]
        stack = []
        print("Found sentence structure : "+str(selectedSentence["input"]))
        
        for action in selectedSentence["stack"]:
            stack.append(action)
        for k in value["databall"]:
            databall[k]=value["databall"][k]
                

        actiondataball = DataBall(ACTIONS=ACTIONS,memory=object_memory,speakmethod=speak,SUBPROCESSES=SUBPROCESSES,subprocesses=subprocesses,tts=tts)

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

            for a in ACTIONS:
                if a.name == actionname:
                    a.setParameters(params)
                    a.action(databall,cc,actiondataball)



def speak(message, tts):
    if type(message) is not str:
        message = str(message)
    message=message.strip()
    print("HSR: "+message)
    if not os.path.exists(os.path.join("voice",message+".wav")):
        count = 0
        for path in os.listdir(os.path.join("voice")):
            if os.path.isfile(os.path.join("voice",path)):
                count=count+1
        print(count)
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