from django.shortcuts import render
from nltk import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import PorterStemmer
import re
from pickle import *

f = open("Lmodel.pkl", "rb")	
model = load(f)
f.close()

f = open("Lvector.pkl", "rb")
tv = load(f)
f.close()


ps = PorterStemmer()
def clean_data(txt):
	txt = txt.lower()
	txt = re.sub("[^A-z ]", "", txt)
	txt = word_tokenize(txt)
	txt = [t for t in txt if t not in punctuation]
	txt = [ps.stem(t) for t in txt if t not in stopwords.words('english')]
	txt = " ".join(txt)
	return txt

def home(request):
	if request.GET.get("title"):
		title = clean_data(request.GET.get("title"))
		author = clean_data(request.GET.get("author"))
		text = title + ' ' + author

		vtext = tv.transform([text])
		news = model.predict(vtext)
		if news[0] == 1:
			msg = "This News is Real"
			return render(request, "home.html", {"msg": msg})
		else:
			msg = "This News is Fake"
			return render(request, "home.html", {"msg": msg})

	else:
		return render(request, "home.html")





