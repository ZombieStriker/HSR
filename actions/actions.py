class AAction:
    def __init__(self, name):
        self.name = name

    def setParameters(self, params):
        """Called to set the parameters of the action. Must be called right before AAction#action()"""
        self.params = params

    def action(self, databall, currentContext,actiondataball):
        """Preforms an action"""
        print("Firing "+self.name)
