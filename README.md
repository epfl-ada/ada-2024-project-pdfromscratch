# Truth behing ratings

## Abstract

A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?

## Research Questions

A list of research questions you would like to address during the project.

## Proposed additional datasets

List the additional dataset(s) you want to use (if any), and some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible.

## Methods

Methods

## Proposed Timeline

Proposed timeline

## Organization within the team

## Instructions

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
