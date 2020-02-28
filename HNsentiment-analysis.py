import boto3
import grequests
import requests 
import statistics
from flask import Flask, request

AWS_ACCESS_KEY_ID="ENTER YOU KEY ID"
AWS_SECRET_ACCESS_KEY="ENTER YOU SECERT KEY"
REGION="ENTER IN WHICH REGION YOU WANT TO RUN THE SERVICE"

HACKER_NEWS_URL="https://hacker-news.firebaseio.com/v0"
FORMAT=".json?print=pretty""

def get_top_stories():
	try:
		URL = HACKER_NEWS_URL+"/topstories"+FORMAT
		r = requests.get(url = URL) 
		return r.json() 
	except:
		return "Error"

def get_comments_of_stories(stories, filter):
	try:
		if stories is "Error":
			return "Error"
		urls = []
		for story_id in stories:
			urls.append(HACKER_NEWS_URL+str(story_id)+FORMAT)
		rs = (grequests.get(u) for u in urls)
		comments_id = []
		comments = grequests.map(rs)
		for comment in comments:
			if comment is not None :
				if filter.lower() in comment.json().get("title").lower().split() and comment.json().get("kids") is not None:
					comments_id.extend(comment.json().get("kids"))
		return comments_id
	except:
		return "Error"

def get_comments_of_comments_group(comments_id_group):
	try:
		urls = []
		for comment_id in comments_id_group:
			urls.append(HACKER_NEWS_URL+str(comment_id)+FORMAT)
		rs = (grequests.get(u) for u in urls)
		comments_text_group = []
		new_comments_id_group = []
		comments = grequests.map(rs)
		for comment in comments:
			if comment is not None :
				comments_text_group.append(comment.json().get("text"))
				if comment.json().get("kids") is not None:
					new_comments_id_group.extend(comment.json().get("kids"))
		return {"new_comments_id":new_comments_id_group,"comments_text":comments_text_group}
	except:
		return "Error"

def get_all_comments(data,comments_text):
	
	comments_text.extend(data.get("comments_text"))

	stop_to_get_data = False if data.get("new_comments_id") is None else True
	while stop_to_get_data:
		new_data = get_comments_of_comments_group(data.get("new_comments_id"))
		if new_data is "Error":
			return "Error"
		comments_text.extend(new_data.get("comments_text"))
		stop_to_get_data = False if not new_data.get("new_comments_id")  else True
		data = new_data

def from_comments_to_setiments(setiments,comments_text):
	comments_text_without_none = []
	for comment in comments_text:
		if comment is not None:
			comments_text_without_none.append(comment)


	for idx in range(0,((len(comments_text_without_none)-1)/25)+1):
		first=idx*25
		last=idx*25+24 if idx*25+24 < len(comments_text_without_none)-1 else len(comments_text)-1
		try:
			client = boto3.client('comprehend',region_name=REGION,aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
			response = client.batch_detect_sentiment(
					TextList=comments_text_without_none[first:last],
					LanguageCode='en'
			)
		except:	
			return "Error"
		for setiment in response[u'ResultList']:
			# print(setiment)
			setiments["AMOUNT"] = setiments["AMOUNT"] + 1
			setiments["POSITIVE"].append(setiment[u'SentimentScore'][u'Positive'])
			setiments["NEGATIVE"].append(setiment[u'SentimentScore'][u'Negative'])
			setiments["NEUTRAL"].append(setiment[u'SentimentScore'][u'Neutral'])
			setiments["MIXED"].append(setiment[u'SentimentScore'][u'Mixed'])

app = Flask(__name__)
@app.route('/sentiment',methods=['GET'])
def hello_world():
	if  len(sys.argv) < 2:
		return "You didn't pass credantials of the AWS account ", 416
	AWS_ACCESS_KEY_ID=sys.argv[0]
	AWS_SECRET_ACCESS_KEY=sys.argv[1]
	REGION="us-east-2" if len(sys.argv) < 3 else sys.argv[2]

	comments = get_comments_of_stories(get_top_stories(),request.args.get('phrase'))
	if comments is "Error":
		return "There is problem with getting data from Firebase", 416
	
	data = get_comments_of_comments_group(comments)
	if data is "Error":
		return "There is problem with getting data from Firebase", 416
	
	comments_text = []
	if get_all_comments(data,comments_text) is "Error":
		return "There is problem with getting data from Firebase", 416

	setiments = {"AMOUNT":0,"POSITIVE":[],"NEGATIVE":[],"NEUTRAL":[],"MIXED":[]}
	if from_comments_to_setiments(setiments,comments_text) is "Error":
		return "There is problem with AWS service", 416
	if setiments['AMOUNT'] == 0:
		return "There is no story titles which contain the phrase : "+request.args.get('phrase') , 416
	return {
		"comments":setiments['AMOUNT'],
			"positive" : {
				"avg":statistics.mean(setiments['POSITIVE']),
				"median":statistics.median(setiments['POSITIVE'])
			},"neutral" :{
				"avg":statistics.mean(setiments['NEUTRAL']),
				"median":statistics.median(setiments['NEUTRAL'])
			},"negative" :{
				"avg":statistics.mean(setiments['NEGATIVE']),
				"median":statistics.median(setiments['NEGATIVE'])
			},"mixed" :{
				"avg":statistics.mean(setiments['MIXED']),
				"median":statistics.median(setiments['MIXED'])
			}
		} , 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

