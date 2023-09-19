# HSR
 Human Speech Robot: A bot designed to listen for speech patterns, and preform actions or speak to the user based on what was said.

# Current Features:

## Sentences and known sentence structures
* "What is ____":
    * The bot will then tell you a summary of the {Thing}.
* "What is the ____ of ____":
    * The bot will then tell you the {Attribute} of the {Thing}
* "What is _____ date":
    * The bot will look up the {Day}'s date, and relay it back to you.
* "What is {Today/Yesterday/Tomorrow}":
    * The bot will look up what day of the way the {Day} is, and relay it back to you.
* "Say ____"
    * The bot will repeat what you say.
* "Tell me a joke"
    * The bot will currently respond that its humor emitters are offline.
        * //TODO: Write Joke Creator 

## Contractions
* Whats -> What is

## Words:
List of known words can be found in the [dictionary.json](dictionary.json).

## Facts
List of known facts about words can be found in the [facts.json](facts.json).

# Planned Features
* Remembering conversation had previously
* Multi-sentence responses.
* Forming own sentences
* ~~"Say ____" sentence structure~~
* "Tell ___ _____" sentence structure
* Responding to its name.
* Renaming the bot.
* Setting local variables to be recalled or commented on later.
* "Remind me _____ in _____" sentence structure
* "Add ____ to the todo list" sentence structure
* "Tell me the todo list" sentence structure

//TODO: Think of more sentence structures and features

# Contributing
If you feel like contributing to this project, you can make a pull request with the changes/additions you want to add. If you want to provide feedback or input on the project, you can create an issue to explain what needs to be fixed, what should be added, or any other feedback you have on the project.