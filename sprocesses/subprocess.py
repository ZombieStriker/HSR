class ASubprocess:
    def __init__(self, name):
        self.name = name

    def setParameters(self, params):
        self.params = params

    # Returns whether the object should be removed from the subprocesses
    def tick(self,databall) -> bool:
        print("Firing "+self.name)
        return True
