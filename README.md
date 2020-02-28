# HackerNews sentiment analysis

HackerNews sentiment analysis is a Python service that provides the user a sentiment analysis of a specific subject in HackerNews top stories comments 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages that are used in the code.

```bash
pip install  boto3          # For use the comprehend service in AWS
pip install  grequests      # For making multiple Async requests from Firebase
pip install  requests 
pip install  statistics     # For the median and average functions
pip install  flask          
```

In my code I chose to work with AWS service for few reasons, first of all, it has the batch option which allows the code to send more then one comment to analyse in one request, which make the code more efficient (less GET requests are send).
The second reason is that it returns exactly the data that I looked for, in oppose to competing products (GCP, Azure). 
For more information about the [sentiment analysis products](https://towardsdatascience.com/machine-learning-as-a-service-487e930265b2)

Another important library that I chose to use is **grequests**, 
This library can take multiple urls and send them parallel, something that reduces the waiting time for response (there are hundreds of requests that are called in the code)

### AWS Credentials:
This solution is using the **boto3** package which should have an AWS account in order to function. This solution is using a hard coded credentials in the source code which you pass to the script, if you want to save your credentials you can find [a more secure  solution](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html) 

## How to use

Run the python script: 
```bash
    sudo python HNsentiment-analysis.py <AWS_ACCESS_KEY_ID> <AWS_SECRET_ACCESS_KEY> [OPTIONAL]<REGION>
```
Send a **GET** request (by the browser / cli):
```
    GET localhost:80/sentiment?pharse=<CHANGE IT BY CUSTOM PRHASE>
```

**Response:**

```
{
    "comments" 123,
    "positive": {
    "avg": 0.57,
    "median": 0.51
    },
    "neutral": {
    "avg": 0.01,
    "median": 0.1
    },
    "negative": {
    "avg": 0.42,
    " median": 0.48
    },
    "mixed": {
    "avg": 0.1,
    "median": 0.12
    }
}
```

## Production solution
### Performance:
If you wish to make your solution more scalable and reduce the amount of requests to AWS service (make it cheaper) you can create an actor which listen to updates and save all the comments and their sentiment in a DB. 
In the DB, every table is a word in a story title (every table contains 2 columns - comments of stories and their sentiments).
When we get a request from the user we will separate it into words, take the tables of these words and intersect between them.
The idea behind this improvement is to make only one call for every comment 

### Change from ip address to URL:
We could use route53 service in AWS in order to map between our machine ip (which we could deploy in AWS) to the url that we want.
