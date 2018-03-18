'''
Project - Feature Based Opinion Mining using Python


** Output will be saved in 'evaluation_output.txt' file.
'''

import re
from nltk import tokenize
#function that loads a lexicon of positive words to a set and returns the set
def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    for line in lex_conn:
        newLex.add(line.strip().replace("\x92","\'"))
    lex_conn.close()

    return newLex

#Function loads features and its synonyms
def loadFeatures(fname):
    feature_synonyms_1=dict()
    
    lex_conn=open(fname)
    for line in lex_conn:
        line = line.strip()
        all_features=line.split(' ')
        
        for feature in all_features:
            feature_synonyms_1[feature]=all_features[0]
    
    lex_conn.close()

    return feature_synonyms_1

#Splitting sentences on stop words
def my_split(s, seps):
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res

#Loading all the lexicons from the files
negation_words=loadLexicon('negation-words.txt') 
features=loadFeatures('features_synonyms.txt')
stop_words=loadLexicon('stop-words.txt')
positive_lex=loadLexicon('positive-words.txt')
negative_lex=loadLexicon('negative-words.txt')


counter=0;

total_correct_orientation=0
overall_total=0

fp = open("input.txt","r") # Input Files
'''
Assuming that the 'text.txt' file contains all the reviews and that too in a single line.
Taking into consideration that a review might contain multiple sentences and those individual sentences
might contain opinions on multiple features.
'''
#write the results to a file
newfile_conn=open('evaluation_output.txt','w')#create a new file and open a connection to it.


# Reading 'text.txt' line by line
for line in fp:
    line = line.lower().strip().replace("\x92","\'")
    '''
    Following statement will split the input line based on '##'
    '''
    structure = line.split('##')
    #Following statement will split the review into individual sentences 
    sentences = tokenize.sent_tokenize(structure[1])
    counter=counter+1
    print '--> review '+structure[0]
    feature_dict=dict()
    manual_test_dict = dict()
    for sentence in sentences:
        
        #Following statement will split the sentences again into individual sub-sentences on the basis of punctuations 
        sub_sentences=re.split('[!?.;]', sentence)
        for sub_sentence in sub_sentences:
            sub_sentence = sub_sentence.strip()
            if sub_sentence != '':
                
                #Following statement will split the sentences again into individual sub-sentences on the basis of
                #stop words like 'and', 'but', 'however' etc.   
                sub_sub_sentences = my_split(sub_sentence, stop_words)
                for sub_sub_sentence in sub_sub_sentences:
                    sub_sub_sentence = sub_sub_sentence.strip()
                    sub_sub_sentence = sub_sub_sentence.replace(',', '')
                    sub_sub_sentence = sub_sub_sentence.replace('!', '')
                    #print "##"+sub_sub_sentence
                    
                    temp_feature_dict=dict()
                    
                    #Now tokenizing the sub-sentence into words
                    words=sub_sub_sentence.split(' ')
                    #print words
                    
                    #Now searching features in the list of words
                    for feature in features:
                        if feature in words:
                            #print " --> " + feature + '['+ features[feature] +']' 
                            temp_feature_dict[features[feature]]=0 
                    
                    
                    # will search opinon only if features are found in that atomic sentence 
                    if len(temp_feature_dict) > 0:
                    
                        orientation=0
                        for word in words:
                            if word in positive_lex:
                                orientation = orientation + 1
                                #Applying Negation Rule here
                                if(words.index(word) != 0):
                                    if words[words.index(word) -1] in negation_words:
                                        #print "Negation Found of positive - "+words[words.index(word) -1]
                                        orientation = orientation - 2
                            if word in negative_lex:
                                orientation = orientation - 1
                                #Applying Negation Rule here
                                if(words.index(word) != 0):
                                    if words[words.index(word) -1] in negation_words:
                                        #print "Negation Found of negative - "+words[words.index(word) -1]
                                        orientation = orientation + 2
                                        
                        for temp_feature in temp_feature_dict:
                            temp_feature_dict[temp_feature]=orientation
                        
                        #print temp_feature_dict
                        
                        
                        for tmp_ftr in temp_feature_dict:
                            if tmp_ftr in feature_dict:
                                feature_dict[tmp_ftr] = feature_dict[tmp_ftr] + temp_feature_dict[tmp_ftr]
                            else:
                                feature_dict[tmp_ftr] = temp_feature_dict[tmp_ftr]
                                
    #Normalizing the 'feature_dict'
    for final_feature in feature_dict:
        if(feature_dict[final_feature] > 1):
            feature_dict[final_feature] = 1
        elif(feature_dict[final_feature] < 0):
            feature_dict[final_feature] = -1
    
    manual_test = structure[2].split('~')
    for feature in manual_test:
        to_enter=feature.split(':')
        manual_test_dict[to_enter[0]]=to_enter[1]
    
    print "Algo Output -- " + str(feature_dict)
    print "Mannual Testing -- " + str(manual_test_dict)
    
    
    
    #Now Comparing the orientation obtained from the algorithm with the orientation obtained by manual testing 
    correct_orientation = 0
    for every_feature in manual_test_dict:
        if every_feature in feature_dict:
            if str(feature_dict[every_feature]) == str(manual_test_dict[every_feature]):
                correct_orientation = correct_orientation + 1
           
    evaluate=str(correct_orientation) + "/" + str(len(manual_test_dict))
    print "Evaluation" + evaluate
    newfile_conn.write("--> "+structure[0] + "\nManual Test Result : " + str(manual_test_dict) + '\nProgram Output: ' + str(feature_dict) + '\nEvaluation: ' + evaluate +"\n\n")    
    
    
    total_correct_orientation=total_correct_orientation+correct_orientation
    overall_total=overall_total+len(manual_test_dict)
    
    print
 

#Total evaluation screening all reviews   
print 'Total accuracy : '+str(total_correct_orientation)+'/'+str(overall_total)
newfile_conn.write('Total accuracy : '+str(total_correct_orientation)+'/'+str(overall_total))
percentage=(float(total_correct_orientation) * 100)/overall_total
print 'Accuracy Percentage --> ' + str(percentage) + "%"
newfile_conn.write('\nAccuracy Percentage --> ' + str(percentage) + "%")
newfile_conn.close()#close the connection 


 
