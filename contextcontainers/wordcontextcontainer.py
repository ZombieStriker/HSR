class WordContextContainer:
    def __init__(self,text):
        self.text=text
        self.tags=[]

    def str(self) -> str:
        temp = ""
        for s in self.text:
            temp = temp+s
        return temp+"{"+str(self.tags)+"}"

    def process(self, dictionary, memory):
        words = self.text
        c_meaning = None
        c_priority = -1

        for d in dictionary:
            xcc = dictionary[d]
            wordsd = xcc["text"].split(" ")
            same = True
            for i in range(0,len(wordsd)):
                if wordsd[i]!=words[i]:
                    same = False
                    break
            if same:
                if c_priority<xcc["priority"]:
                    c_priority = xcc["priority"]
                    c_meaning=xcc
        if c_meaning:
            self.meaning=c_meaning
        else:
            for d in dictionary:
                xcc = dictionary[d]
                if(xcc["text"]=="NULL"):
                    self.meaning=xcc
                    break
        try:
            self.tags = self.meaning["tags"]
        except:
            self.tags=[]
        if c_meaning:
            self.meaning=c_meaning
            self.wordsLen = len(self.meaning["text"].split(" "))
            self.text=self.text[:self.wordsLen]
        else:
            self.wordsLen = 1
            self.text=self.text[:self.wordsLen]
            self.meaning = {
                "text":self.text,
                "priority":-1,
                "tags":["UNKNOWN"]
            }
            x = {}
            x["name"] = self.text[0]
            memory[x["name"]]=x

            if self.text[0].isnumeric():
                if not "tags" in x:
                    x["tags"] =[]
                x["tags"].append("NUMBER")
                self.tags.append("NUMBER")