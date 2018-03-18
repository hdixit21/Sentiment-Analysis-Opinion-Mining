# Sentiment-Analysis-Opinion-Mining

## OBJECTIVE
Too many reviews online that it’s difficult to read them all. This project will be able to analyze these reviews and list the opinion of the user as positive or negative for a list of features.

## DATASET
Using yelp restaurant reviews. Number of reviews used in project: 200

## OUTPUT
Output will be saved in a new file by name “evaulation_output.txt”

### Lexicons used
Manually reviewed yelp restaurant reviews to build below mentioned list:

```
List of features & their Synonyms (“features_synonyms.txt”)
Negation Word-: no, not, never, doesn’t, isn’t, wasn't (“negation-words.txt”)
Stop words-: but, and, although, however, than (“stop-words.txt”)
Negative Words: Provided by Professor (“negative-words.txt”)
Positive Words: Provided by professor (“positive-words.txt”)
```

### Format of dataset
Total No. of Reviews: 200
Each line in the document is a single review
At the end of each review, it list all the features present in that particular review with its orientation separated by single "~". 
Dealing with two types of orientation

```
Positive (1)
Negative (-1)
Ex: “Sentence1##The steak was good but the service was not good. ##Steak:1~ service: -1”
Name of Dataset file: “input.txt”
```

### Features & synonyms
```
place: restaurant joint experience
ambiance: vibes decor atmosphere environment
service: staff server servers delivery
drinks:wine drinks cocktails
meat: steak chicken shrimp beef lamb fish
food: taste pizza salad burger potatoes buffet dishes meal flavour pasta mofongo tacos
people: gesture chef bartender waitstaff server
price: cost pricey costly value
```

### Deciding orientation for reviews
```
Ex. “Food and service both were good.”
	For this orientation for Food =1, service =1 (No other features will be listed. Features that appear in that review only will be listed in front of review with its orientation.)
Ex. “ The food was really amazing.”
	For this, orientation for Food = 1. Having “really” before amazing does not mean we will give it an extra point. Orientation for food will remain 1 only.The magnitude of the feature is not considered. Final opinion can be only positive or negative.
Ex: “The restaurant has amazing taste.”
	Taste is a synonym of food and restaurant is a synonym of place. The main features for these are food and place respectively. So place and food will be marked as positive by assigning value 1.
```

### Understanding Algorithm
#### Step 1: Breaking the dataset
```
The code will first split each review into atomic sentences based on:
Split the sentences on “period”.
Split on “punctuations (?,!,;)” 
Split on “stop words (but, however, although, etc.)”
```

#### Step 2-Deciding orientation
```
Creates a list of features and opinion words for every atomic sentence.
Takes average of orientation(positive=1, negative=-1) of each opinion words in one sentence and assign it to each feature in that sentences.
Ex: “Service was good, nice ambiance.” 
	Service and ambiance both will be assigned positive orientation i.e 1.
	“The steak was good. The service was not good.”
	‘Not’ here is negation word so positive word “good” will be changed to negative opinion for service.
```

### List of files:
```
1. SentimentAnalysis.py : The main executable file. 
2. input.txt : The file contains all the 200 reviews along with manual testing results. (Note: reviews and manual testing result are separated by '##' ) 
3. features_synonyms.txt : Contains a list of all features with their synonyms. 4. stop-words.txt : Contains the list of all stop/transition words like 'but', 'although', 'however' etc. 
5. negation-words.txt : Contains a list of all the words that reverses the orientation of opinion words. 
6. negative-words.txt: Contains the list of all the words that have negative orientation. 
7. positive-words.txt: Contains the list of all the words that have positive orientation. 
8. evaluation_output.txt : Shows the final output and the overall accuracy of the algorithm.
```
