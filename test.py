##def findAll(wordList, lStr):
##    final_list = []
##    for word in wordList:
##        for i in range(len(word)):
##            if word[i] in word[i+1:]:
##                break
##            for j in word:
##                if j not in lStr:
##                    break
##
##            final_list.append(word)
##
##    return final_list
##
##
##
##samplelist = ['babies', 'momma', 'hello', 'word', 'code', 'jesus', 'barbeque']
##
##letters = 'edoc'
##
##print findAll(samplelist, letters)
