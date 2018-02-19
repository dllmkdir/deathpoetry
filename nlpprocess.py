import csv
import sys
maxInt = sys.maxsize
decrement = True
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

from nltk.tokenize import RegexpTokenizer
import nltk
from nltk.corpus import wordnet

from nltk.corpus import stopwords
poemc=0
negativec=0#negative connotations counter
intensityc=0#intensity counter
intensitycli=0#intensity counter comparision
poemflag=True
poemarray=list()
dumpstring=""
while decrement:
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True
with open('deathpoet.csv','rb') as csvfile:
	csvread=csv.reader(csvfile, delimiter=' ', quotechar='|')

	for row in csvread:
		trims=' '.join(row).strip()#trimmed string
		if(trims =='\"'):
			poemc+=1
			if(poemflag==True):
				poemarray.append(dumpstring.decode('utf-8'))#dump poem into poem array
				dumpstring=""
				poemflag=False

			else:
				pass	
		else:
			dumpstring+=str(trims)#unnecesary cast...
			poemflag=True
			#print(trims)
del poemarray[0]
print(poemc/2) #number of poems = 2100
print(len(poemarray)) #number of poems
print(poemarray[0]) #number of poems
print(poemarray[-1]) #number of poems
deathc=0

synolist=list()#create synonims list
deathsyn=  wordnet.synsets("Death")
for x in deathsyn:
	for lemma in x.lemmas():
		synolist.append(lemma.name())
print(synolist)
sid = SentimentIntensityAnalyzer()
sumneg=0#negative average
freqlist=nltk.FreqDist({})
poemstrings=list()#total poems in one string
stoplist = stopwords.words('english')
for poem in poemarray:#find death referrences in synonim list
	if not poem:#for any reason, if the poem is empty, then continue to the next one
		continue

	#print("-------------------------------")
	if any(x in poem for x in synolist):
#	if "death" in poem
			
		tokenizer = RegexpTokenizer(r'\w+')
		tokens=tokenizer.tokenize(poem)#tokenize alphanumeric content
		clean_tokens_temp= tokens[:]
		for token in tokens:
			if token!="I" and ((token.lower() in stoplist) or (token.lower() =='bcolor') or (token.lower() =='transparent') or (token.lower() =='ffffff')):#remove stopwords
				clean_tokens_temp.remove(token)
		#print(clean_tokens_temp)
		deathc+=1
		freq = nltk.FreqDist(clean_tokens_temp)
		freqlist+=freq
		poemstrings.extend(clean_tokens_temp)
		sentimento=sid.polarity_scores(poem)
		for k in sorted(sentimento):
			if(k=='neg'):
				#print("Average negativity: "+str(sentimento[k]))
				negativec+=sentimento[k]

			if(k=='compound'):
				#print("Average polarity: "+str(sentimento[k]))
				intensityc+=sentimento[k]#
nltkpoem=nltk.Text(poemstrings)
freqlist.plot(50,cumulative=False)

nltkpoem.dispersion_plot(["death","decease","expiry","dying","demise","last","end","destruction"])

print("Death related poems: "+ str(deathc))#796
print("Negative connotations: "+str(negativec/deathc))#0.0678155835318
#0.0561160627785
print("Intensity average with death related poems: "+str(intensityc/deathc))#0.10297522967
#0.0695253633017
