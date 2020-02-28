# HackerNews sentiment analysis

HackerNews sentiment analysis is a Python service which let the user the ability to get the sentiment analysis of specific subject in  HackerNews top stories comments 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages which we using in the code.

```bash
pip install  boto3
pip install  grequests
pip install  requests 
pip install  statistics
pip install  flask 
```
### AWS Credantials:
This solution using the **boto3** package which should have an AWS account for using it. this solution using an hard coded credentials in the source code which you passing to script, but if you want to save your credentials you could find [more secure  solution](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html) 

## How to use

You should run the python script: 
```bash
python HNsentiment-analysis.py AWS_ACCESS_KEY_ID   AWS_SECRET_ACCESS_KEY    [OPTIONAL] REGION
 ```
and then all you have to do is sent GET request (by the browser / cli) to:
```
GET localhost:80/sentiment?pharse=<CHANGE IT BY CUSTOM PRHASE>
```
and the response will look like:

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

## production solution
### Performance:
If you want to make your solution more scalable and reduce the amount of requests to AWS service (make it cheaper) you could make an actor which listen to updates and save all the comments and their sentiment in DB when every table is word in story title (and contains all the comment of stories which contains this word in the title).
when we get a request from the user we will separate it to words and we will take the tables of this words and intersect between them.

The idea behind this improvement is to make one call for every comment instead more then one (we will prefer this when there is a lot of users and the probability to analyse every comment is very high).

### Change from ip address to URL:

we could use route53 service in AWS to map between our machine ip (which we could deploy in AWS) to the url that we want.
