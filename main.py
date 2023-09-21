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

    speak("HSR online",tts)
    while True:

        subprocessDataball = DataBall(ACTIONS=ACTIONS,memory=object_memory,SUBPROCESSES=SUBPROCESSES,subprocesses=subprocesses,speakmethod=speak,tts=tts, parsemethod=parseString, wordprocessingmethod=findRightMeaning)
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
        

        listOfSentenceChecks = parseString(words=words,meaninglist=cc)
        

        if len(listOfSentenceChecks) == 0:
            print("No sentences matched :(")
            continue
        value = listOfSentenceChecks[random.randint(0,len(listOfSentenceChecks)-1)]
        selectedSentence = value["jj"]
        stack = []
        print("Found sentence structure : "+str(selectedSentence["input"]))
        
        for action in selectedSentence["stack"]:
            stack.append(action)
        for k in value["databall"]:
            databall[k]=value["databall"][k]

        databall["deep"] = 1
                

        actiondataball = DataBall(ACTIONS=ACTIONS,memory=object_memory,speakmethod=speak,SUBPROCESSES=SUBPROCESSES,subprocesses=subprocesses,tts=tts,parsemethod=parseString, stack=stack, wordprocessingmethod = findRightMeaning)

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
        for j in library:
            jj = library[j]
            isPattern = True
            index = 0
            wordindex = 0

            foundwords = 0
            nonoptional_words = 0
            optional_words = 0

            starOperator = False
            hasStarOperator = False
            tdataball = {}

            #First determine how many optional words, non-optional words there are and whether there is a star operator
            for inputWords in jj["input"]:
                if inputWords.startswith("*") or inputWords.startswith("?*"):
                    hasStarOperator = True
                    nonoptional_words+=1

                elif not inputWords.startswith("?"):
                    nonoptional_words=nonoptional_words+1
                else:
                    optional_words=optional_words+1
            

            #Loop through all the input words, to see if the words match the sentence structure
            for inputWords in jj["input"]:
                    
                #If the input word has a name, add its index (where it is) to the databall
                if(inputWords.count(":")>0):
                    inputsplit = inputWords.split(":")
                    inputWords=inputsplit[0]
                    tdataball["var_"+inputsplit[1]] = wordindex

                #If the input word is the star operator, then skip to the next word and check if it is the next required/non-optional input word
                if inputWords == "*":
                    if(starOperator):
                        index=index+1
                        continue
                    starOperator=True
                    lenthOfVar = 0   
                    index=index+1
                    continue


                #if its in star operator mode, keep looping until you get all the words that match up until the next required/non-optional word
                if starOperator:                     
                    while starOperator:        
                        isQuestionable = False
                        if len(meaninglist) <= index:
                            lenthOfVar+=1
                            print("Breaking because length of meaninglist is less than index ("+str(index)+"+"+str(lenthOfVar)+")")
                            if not "varlen_"+inputsplit[1] in tdataball:
                                print(str(lenthOfVar)+"=====================================================")
                                tdataball["varlen_"+inputsplit[1]] = lenthOfVar
                            break
                        if(len(words) < index+lenthOfVar):
                            wordindex-=1
                            index-=1
                            print("Breaking because The list of words is less than ("+str(index)+"+"+str(lenthOfVar)+")")
                            if not "varlen_"+inputsplit[1] in tdataball:
                                tdataball["varlen_"+inputsplit[1]] = lenthOfVar-index
                            break
                        if(len(words) == index+lenthOfVar):
                            print("Breaking because The list of words is EQUAL to ("+str(index)+"+"+str(lenthOfVar)+")")
                            if not "varlen_"+inputsplit[1] in tdataball:
                                tdataball["varlen_"+inputsplit[1]] = lenthOfVar-index
                            break
                        meanings=meaninglist[index+lenthOfVar]
                        foundwords+=1
                        if  inputWords.startswith("?"):
                            inputWords = inputWords[1:]
                            isQuestionable = True

                        tagfound = False
                        if not tagfound:
                            for name in meanings.text:
                                if inputWords == name:
                                    tagfound=True

                        if not tagfound:
                            for tags in meanings.tags:
                                if inputWords == "{"+tags+"}":
                                    tagfound=True
                                    break

                        if tagfound:
                            if not "varlen_"+inputsplit[1] in tdataball:
                                tdataball["varlen_"+inputsplit[1]] = lenthOfVar-index
                            index=index+1 
                            starOperator = False
                            wordindex-=1
                        else:
                            lenthOfVar=lenthOfVar+1  
                            wordindex+=1

                    if(starOperator):
                        continue

                else:
                    isQuestionable = False
                    if len(meaninglist) <= index:
                        continue
                    meanings=meaninglist[index]

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
                             wordindex+=1
                    elif not tagfound:
                        isPattern=False
                        continue
                    else:
                        foundwords=foundwords+1
                        wordindex+=1

            if starOperator:
                starOperator=False
                index-=1
                lenthOfVar=len(meaninglist)-index
                lenthOfVar-=1
                print(str(jj["input"])+"  "+str(index)+"   -----------    "+str(foundwords)+"/"+str(lenthOfVar)+"  -=- "+str(len(meaninglist))+"       "+str(words))
                if not "varlen_"+inputsplit[1] in tdataball:
                    tdataball["varlen_"+inputsplit[1]] = lenthOfVar-index

            
            if not hasStarOperator:
                if not (foundwords>= nonoptional_words and ((foundwords <= nonoptional_words+optional_words))):
                    #print("Not same length: "+str(foundwords)+" ["+str(nonoptional_words)+", "+str(nonoptional_words+optional_words)+"]")
                    continue


            if isPattern:
                if index == len(meaninglist) or hasStarOperator:
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
        return listOfSentenceChecks



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