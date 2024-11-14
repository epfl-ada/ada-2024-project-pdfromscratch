# Truth behing ratings

## Abstract

A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

## Research Questions

A list of research questions you would like to address during the project.

### 1. How can we quantify users' knowledge of beer?

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

### 2. Are users influenced by the past rating of the beer ?

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

### 3. Are users influenced by their past ratings ?

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

### 4. Are text reviews and user scores consistent with each other?

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

### 5. Are users influenced by current trends in beer consumption ?

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

## Proposed additional datasets

Current review data on the BeerAdvocate website ranges from August 1996 to August 2017. We thought of developing a scraper to retrieve more recent data from August 2017 to today. Nevertheless, after a preliminary analysis, we encountered more technical pitfalls. The site requires users to be authenticated to consult reviews, and imposes a rate limit on queries, which could complicate information retrieval.

## Methods


All analysis will be conducted over different user and beer segments such as user country, user knowledge, beer country or beer style.

### 1. How can we quantify users' knowledge of beer?

We will try to use different features and combination of features to derive a notion of beer knowledge for each user at different points in time.

A first approach we considered is to use the Gini Impurity on the distribution of beer styles in the beer rated by each user at a given time. This would give us a value in $[0,1]$ measuring the diversity of beer styles rated by each user and therefore an estimate of its ability to accurately rate a wide range of beers.

<span style="background-color: red; color: white; padding: 0.4rem">TODO (JEAN) : check Gini explaination</span>

Another approach is to analyze the number of ratings and the user's review rate (number of reviews per unit of time). More specifically, looking at the timeframe during which the user was active on the website.

A further method would be to analyze the texts backing up the ratings, assuming that the length of the text and the use of  keywords from the beer lexical field would be a good indicator of knowledge. This list of keywords would be created manually by researching the beer industry.

### 2. Are users influenced by the past rating of the beer ?

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

OLS + F_test => effect mixed

### 3. Are users influenced by their past ratings ?

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

### 4. Are text reviews and user scores consistent with each other?

In order to compare the similarity of textual reviews and scores, we will use an NLP model for sentiment analysis. More specifically, we found the model `nlptown/bert-base-multilingual-uncased-sentiment` which predict the sentiment of a review as an integer in $[1,5]$ which corresponds to the same range as the scores given by the users.

We will then use a distance metric to analyze the disparency between the text and the score. Those differences could be assesed using hypothesis testing where null hypothesis would be that their is no difference between means.

### 5. Are users influenced by current trends in beer consumption ?

t-test on ratings distribution of beer styles during trends and outside trends (assessment of global effect on population)

OLS to measure impact of trends on ratings : trend_ratings = alpha + beta * no_trend_ratings ?

Add it to the previous OLS ?

Should trend take the ratings in addition to the ratings rate ?

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

## Proposed Timeline

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

| Period | Description |
|---|---|
| Week 1 : 18/11 - 24/11 | |
| Week 2 : 25/11 - 01/12 | |
| Week 3 : 02/12 - 08/12 | |
| Week 4 : 09/12 - 15/12 | |
| Week 5 : 16/12 - 20/12 | |

## Organization within the team

<span style="background-color: red; color: white; padding: 0.4rem">TODO : explain</span>

## Instructions

<span style="background-color: red; color: white; padding: 0.4rem">TODO : preprocessing</span>

Please download the datasets by folowing these commands :
```bash
cd src/scripts
python download.py
cd ../../
pip install -r pip_requirements.txt
```

## Project Structure

```
├── data                        <- Project data files
│
├── src                         <- Source code
│   ├── data                            <- Data directory
│   ├── models                          <- Model directory
│   ├── utils                           <- Utility directory
│   ├── scripts                         <- Shell scripts
│
├── tests                       <- Tests of any kind
│
├── results.ipynb               <- a well-structured notebook showing the results
│
├── .gitignore                  <- List of files ignored by git
├── pip_requirements.txt        <- File for installing python dependencies
└── README.md
```
