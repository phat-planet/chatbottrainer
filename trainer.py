import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import time

logging.basicConfig(level=logging.INFO)

# Upon running for the first time, you need to edit chatbottrainer\venv\Lib\site-packages\sqlalchemy\util\compat.py
# go to line 264, replace time.clock with time.process_time()

# if running python 3.10(?), you will have to edit another file, to go
# chatbotTrainer\venv\lib\site-packages\yaml\constructor.py, replace line 126 with:
# if not isinstance(key, collections.abc.Hashable):

chatbot = ChatBot("spork")
name = "User"
bad_words = ['jabroni', 'doofus', 'dumbass', 'pinhead']  # the bot will not say phrases containing these words

while True:
    choice = input('Run in read-only mode? Enter Y/N: ')  # sfx option
    if choice == 'Y' or choice == 'y' or choice == 'yes':
        ROselect = True
        break
    if choice == 'N' or choice == 'n' or choice == 'no':
        ROselect = False
        break

bot = ChatBot(  # defining properties and attributes
    'spork',
    read_only=ROselect,
    storage_adapter='chatterbot.storage.SQLStorageAdapter',  # this defines the database the bot will use to learn
    preprocessors=[  # these will clean up the text so the bot can understand
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    logic_adapters=[
        {
            'import_path': 'similar_response.SimilarResponseAdapter',
            'input_text': 'What is my name?',
            'output_text': ('Your name is ' + name + '.'),
            'similarity_threshold': 0.7
        },
        {
            'import_path': 'similar_response.SimilarResponseAdapter',
            'input_text': 'What is your name?',
            'output_text': 'I don\'t have one, at the moment.',
            'similarity_threshold': 0.7
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',  # if the bot can't think of a response, it will give a
            'default_response': 'Sorry, I don\'t quite understand.',  # default response
            'maximum_similarity_threshold': 0.6,
            'excluded_words': bad_words
        },

        'chatterbot.logic.MathematicalEvaluation',  # this gives the bot the ability to solve math equations
        {
            'import_path': 'newtime_adapter.NewTimeLogicAdapter',  # this gives the bot the ability to tell time
        }

    ],
    database_url='sqlite://database.sqlite3'
)
print('Starting bot. . . . ')

print('Do not train the bot more than once; It clutters the database with repetitive input/response.')
print('Delete or move the database somewhere else if you want to train again.')
while True:
    choice = input("Would you like to train the bot? Enter Y/N: ")  # train bot option
    if choice == 'Y' or choice == 'y' or choice == 'yes':
        ##################################
        #           BOT TRAINING         #
        ##################################
        print('Training bot. . . . . .')
        trainer = ListTrainer(bot)
        # list trainer
        trainer.train([ # ListTrainer will train words from the code, you are better off editing or making new YAML file
            "Hello",
            "Hi there!",
            "How are you doing?",
            "I'm doing great.",
            "That is good to hear",
            "Thank you.",
            "You're welcome."
        ])
        trainer.train([  # this is for testing excluded words, the bot isn't supposed to insult you!
            "Insult me",
            "You're a dumbass."
        ])
        trainer.train([
            "Ask me about my mood",
            "How are you feeling?",
            "I am feeling",
            "So you're feeling? Did I get that right",
            "Yes",
            "Great!"
        ])
        trainer.train([
            "Ask how I'm feeling",
            "How are you feeling?"
        ])
        trainer.train([
            "How are you feeling?",
            "I am feeling",
            "So you're feeling? Did I get that right",
            "No",
            "Oh. That's ok, I'm still learning."
        ])
        # training files are at chatbottrainer\venv\Lib\site-packages\chatterbot_corpus\data\english
        # add custom files to the 'custom' folder
        trainer = ChatterBotCorpusTrainer(bot)
        trainer.train(
            "chatterbot.corpus.english",
            "chatterbot.corpus.custom.mood"
            "chatterbot.corpus.custom.misc"
        )
        ##################################
        #         END OF TRAINING        #
        ##################################
        break
    if choice == 'N' or choice == 'n' or choice == 'no':
        break
print('Chatbot is now active')

while True:
    try:
        print('User: ', end='')
        request = input()
        # print(name + ': ' + request)
        if request == "Bye" or request == 'bye' or request == 'goodbye' or request == 'Goodbye' or request == 'shut up':
            print('Chatbot: Bye. Shutting down. . . .')  # if you say these things to the bot, it will quit
            break
        else:
            response = bot.get_response(request)
            print("Chatbot: ", end='')
            print(response)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break
