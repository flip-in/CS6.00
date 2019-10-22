# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):

    def __init__(self, guid, title, subject, summary, link):

        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
    

    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

###WordTrigger###
class WordTrigger(Trigger):

    def __init__(self, word):

        self.word = word
        
    '''
    ###not needed?###
    def get_word(self, word):
        return self.word
    ''' 

    def is_word_in(self, text):
        word = self.word.lower()
        text = text.lower()
        #remove punctuation and replace with ''
        replace_punctuation = string.maketrans(string.punctuation, \
                                               ' '*len(string.punctuation))
        text = text.translate(replace_punctuation)
        text_words = text.split()
        
        return word in text_words

###TEST###        
##word1 = WordTrigger('Soft')        
##test1 = 'Koala bears are soft and cuddly.'
##test2 = 'I prefer pillows that are soft.'
##test3 = "Soft's the new pink!"
##test4 = 'Soft drinks are great.'
##test5 = '"Soft!" he exclaimed as he threw the football.'
##test6 = 'Microsoft announced today that pillows are bad.'
##
##print word1.is_word_in(test1)
##print word1.is_word_in(test2)
##print word1.is_word_in(test3)
##print word1.is_word_in(test4)
##print word1.is_word_in(test5)
##print word1.is_word_in(test6)
###END TEST###
    
###TitleTrigger###


class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_title())
   
###Test###
word1 = 'intel'        
story = NewsStory('test guid', \
                  'Intel Accused of Using Minature Monkeys to Power Microprocessors'\
                 ,'test subject', 'test summary', 'test link')

''' other ways to test TitleTrigger '''
'''
##print TitleTrigger.evaluate(TitleTrigger(word1), story) # First Way
##test = TitleTrigger(word1) #Second Way
##print test.evaluate(story) #Second Way
'''
print TitleTrigger(word1).evaluate(story) #Third Way?
###END TEST###

# TODO: SubjectTrigger

class SubjectTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_subject())
    
# TODO: SummaryTrigger

class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_summary())


# Composite Triggers
# Problems 6-8


# TODO: NotTrigger

class NotTrigger(Trigger):

    def __init__(self, other_trigger):
        self.other_trigger = other_trigger

    def evaluate(self, newsitem):
        return not self.other_trigger.evaluate(newsitem)

###TEST###
Test = TitleTrigger(word1)
print NotTrigger(Test).evaluate(story)
###END TEST###

# TODO: AndTrigger

class AndTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, newsitem):
        return self.trigger1.evaluate(newsitem) and self.trigger2.evaluate(newsitem)
    
# TODO: OrTrigger

class OrTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, newsitem):
        return self.trigger1.evaluate(newsitem) or self.trigger2.evaluate(newsitem)
    

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger

class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
##        if self.phrase in story.get_title():
##            return True
##            
##        if self.phrase in story.get_subject():
##            return True
##            
##        if self.phrase in story.get_summary():
##            return True
##
##        else:
##            return False
        return self.phrase in story.get_title() \
               or self.phrase in story.get_subject() \
               or self.phrase in story.get_summary()
            
        

###======================
### Part 3
### Filtering
###======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    # Feel free to change this line!
    filtered_stories = []
    
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) == True:
                filtered_stories.append(story)
                break
    
    return filtered_stories

###======================
### Part 4
### User-Specified Triggers
###======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    triggers = []
    triglist = []
    trig_dict = {}
    
    for line in lines:
        triglist = line.split()
        if triglist[1] == 'SUBJECT':
            trig_dict[triglist[0]] = SubjectTrigger(triglist[2])
            
        elif triglist[1] == 'TITLE':
            trig_dict[triglist[0]] = TitleTrigger(triglist[2])
            
        elif triglist[1] == 'SUMMARY':
            trig_dict[triglist[0]] = SummaryTrigger(triglist[2])
                      
        elif triglist[1] == 'PHRASE':
            trig_dict[triglist[0]] = PhraseTrigger(triglist[2:])
                      
        elif triglist[1] == 'OR':
            trig_dict[triglist[0]] = OrTrigger(trig_dict[triglist[2]], \
                                                 trig_dict[triglist[3]])
                      
        elif triglist[1] == 'AND':
            trig_dict[triglist[0]] = AndTrigger(trig_dict[triglist[2]], \
                                                 trig_dict[triglist[3]])

        elif triglist[1] == 'NOT':
            trig_dict[triglist[0]] = NotTrigger(trig_dict[triglist[2]])

        elif triglist[0] == 'ADD':
            for trigs in triglist[1:]:
                triggers.append(trig_dict[trigs])                                                
                    
    return triggers
    
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

