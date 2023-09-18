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

print("Loading dictionaries, libraries, and facts...")
dictionary = json.loads(open(os.path.join("dictionary.json"),"r").read())
library = json.loads(open(os.path.join("library.json"),"r").read())
facts = json.loads(open(os.path.join("facts.json"),"r").read())
contractions = json.loads(open(os.path.join("contractions.json"),"r").read())

object_memory = {}
object_facts = {}

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




def getVoice():
    with sr.Microphone() as source:
        r = sr.Recognizer()
        r.energy_threshold=450
        text = ""
        try:
            temp = r.listen(source=source,timeout=1)
            try:
                text = r.recognize_google(temp)
            except:
                print("Error")
        except:
            return ""
    return text.lower()

def findRightMeaning(words, index):
    wordsEnd = words[index:]
    
    cc = WordContextContainer(wordsEnd)
    cc.process(dictionary)

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
        
        for j in library:
            jj = library[j]
            isPattern = True
            index = 0

            foundwords = 0
            nonoptional_words = 0
            optional_words = 0

            for inputWords in jj["input"]:
                if not inputWords.startswith("?"):
                    nonoptional_words=nonoptional_words+1
                else:
                    optional_words=optional_words+1
            for inputWords in jj["input"]:

                if(inputWords.count(":")>0):
                    inputsplit = inputWords.split(":")
                    inputWords=inputsplit[0]
                    databall["var_"+inputsplit[1]] = index

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
            
            if not (foundwords>= nonoptional_words and foundwords <= nonoptional_words+optional_words):
                print("Not same length: "+str(foundwords)+" ["+str(nonoptional_words)+", "+str(nonoptional_words+optional_words)+"]")
                continue


            if isPattern:
                if index == len(cc):
                    if(lastjj == None) or len(jj["input"])>=len(lastjj["input"]):
                        stack = []
                        for action in jj["Stack"]:
                            stack.append(action)
                        lastjj = jj
                

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
                    a.action(databall,cc,object_memory,tts,speak)



def speak(message, tts):
    message=message.strip()
    print("HSR: "+message)
    if not os.path.exists(os.path.join("voice",message+".wav")):
        tts.tts_to_file(message+".", file_path="voice/"+message+".wav")
    init = AudioSegment.from_wav("voice/"+message+".wav")
    play(init)


main()