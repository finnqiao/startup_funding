# Startup Success Metrics for Venture Capital Firms

- [Product Charter](#product-charter)
	* [Mission](#mission)
	* [Vision](#vision)
	* [Success Criteria](#success-criteria)
- [Repo Structure](#repo-structure)
- [Running the application](#running-the-application)
	* [1. Set up environment](#1-set-up-environment)
	* [2. Create database locally or in RDS](#2-create-database-locally-or-in-rds)
	* [3. Make necessary files and trained model](#3-make-necessary-files-and-trained-model)
	* [4. Run flask app](#4-run-flask-app)
	* [5. Further unit testing](#5-further-unit-testing)
- [Planned Work](#planned-work)
- [Backlog](#backlog)
- [Icebox](#icebox)

Scenario analysis of venture capital outcomes based on startup characteristics, funding history, and macroeconomic conditions.

## Product Charter

Primary focus of the app is to inform startups and venture capital funds alike on different startup success metrics like exit probabilities and funding amounts.

### Vision

Improve risk management by venture capital firms and fundraising decisions by startups.

### Mission

Utilize past venture outcomes to predict startup success on a variety of metrics like fundraising and exit opportunities.

### Success Criteria

R2 of at least 0.5 due to the inaccuracies of funding predictions.

Inbound traffic from 100 existing venture capital firms and 60% retention thereafter.

## Repo structure

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── app.py                        <- File to run Flask app from
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│   ├── model_config.py               <- Configuration files for data and model training
│   ├── flask_config.py               <- Configuration files for flask app
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git.
│   ├── auxiliary/                    <- Place to put intermediate transformed and merged data. Not synced with git.
│   ├── external/                     <- External data sources,not synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others.
│   ├── archive                       <- Develop notebooks no longer being used.
│
├── src                               <- Source data for the project
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files
│   ├── sql/                          <- SQL source code
│   ├── ingest_data.py                <- Script for downloading data from source.
│   ├── clean_companies_data.py       <- Script for cleaning and feature generation for company data.
│   ├── clean_investors_data.py       <- Script for cleaning and feature generation for investors data.
│   ├── clean_acquisitions_data.py    <- Script for cleaning and feature generation for acquisitions data.
│   ├── clean_rounds_data.py          <- Script for cleaning and feature generation for rounds data.
│   ├── clean_macro_data.py           <- Script for cleaning and feature generation for macro data.
│   ├── preprocess_merge_data.py      <- Script for merging cleaned datasets.
│   ├── train_model.py                <- Script for training, scoring, and uploading model to S3.
│
├── test                              <- Files necessary for running model tests (see documentation below)
│
├── Makefile                          <- Makefile to generate required data files and model
├── requirements.txt                  <- Python package dependencies
```

## Running the application

### 1. Set up environment

The `requirements.txt` file includes packages required for the code. The environment can be set up with conda with the following code:
```
conda create -n startup_funding python=3.7
conda activate startup_funding
pip install -r requirements.txt
```

### 2. Create database locally or on RDS

The file `create_database.py` creates the database. To do so, make sure you are in the startup_funding root folder and run the following command:
```
python src/sql/create_database.py
```

This will create a local database in the data folder.

Alternatively, should a RDS database be preferred, make sure RDS configurations are in place and run the following command:
```
python src/sql/create_database.py --RDS=True
```

### 3. Make necessary files and trained model

Before running make all, ensure a new S3 bucket is set up to receive transformed data files and pickled model. Make sure that the name of your S3 bucket is `startup-funding-working-bucket` as that is the default bucket name that the data is saved to.

From the root startup_funding directory, run `make all`.

This will download all raw data files, save them to a specified S3 bucket based on configurations, clean and feature generate from the raw data, save transformed data locally and in a specified S3 bucket, train a model, and save the trained model locally and in a specified S3 bucket.

For generating individual transformed data files or the pickled model file, refer to the make commands within `Makefile`.

### 4. Run flask app

With the necessary data and model in place, run `flask run --host=‘0.0.0.0’ --port=‘5000’`

The flask app can now be accessed at the listed url through the specified port (5000).

### 5. Further unit testing

Pytest testing scripts have been set up in the test folder.

To run each test file, run `pytest [testing_file.py]` on the command line.

The following test files are available:

1. cleaning_test.py	<- Unit test for all cleaning scripts
2. merge_data_test.py	<- Unit test for merging all cleaned data
3. gen_helpers_test.py	<- Unit test for general helpers
4. nlp_helpers_test.py	<- Unit test for natural language processsing related functions
5. model_test.py	<- Unit test for functions within model train

## Planned Work

Detailed project tracker on: https://airtable.com/shraRLvLq3cHHVX9p

### Theme 1: A dataset that is effective in representing every facet of the venture capital ecosystem 

- E1 - Aggregate general startup data during time period
	- S1 : Cleaned data on general information for each startup 
	- S2 : New features based on funding frequencies, amounts, target market.
- E2 - Venture round trends and characteristics
	- S3 : Cleaned data on venture rounds that were raised by startups during this period.
	- S4 : New features based on the type of venture round that was raised - seed, growth etc.
	- S5 : Venture type and amount trends across time period.
- E3 - Data on venture capital investors who invested during time period
	- S6 : Cleaned data on venture investors during time period.
	- S7 : Scoring of venture investors based on frequency, amount of fundings.
	- S8 : Social media and online mention frequency and influence of venture capital investors.
- E4 - Mergers and acquisitions that happened to companies in question
	- S9 : Cleaned data on mergers and acquisitions during this period.
	- S10 : New features based on how accretive acquisition was.
	- S11 : Success metric and scoring to gauge venture outcome.
- E5 - Macro environment and trends during time period
	- S12 : Acquired external data on macro trends during time period.
	- S13 : Cleaned data on external macro trends.
	- S14 : New features based on how macro trends compare across different time periods.

### Theme 2: Machine learning models that help predict different venture outcomes

- E6 - Predict total funding amount of startup
	- S15 : Grouped, aggregated, and in-depth EDA across all collected data.
	- S16 : New features from combined datasets.
	- S19 : Base regression model for funding amounts.
	- S20 : Model selection and model tuning for regression model on funding amounts.
- E7 - Predict startup/venture outcome - whether is still operating, acquired, went public
	- S17 : Base logistic regression model for multilabel classification.
	- S18 : Model selection and model tuning for multilabel classification.
	- S21 : Estimate valuation of startup based on combination of predictive models.

### Theme 3: Intuitive interface for venture capital firms and startups alike to gather outcomes from predictive models

- E8 - User interface for predicting startup outcomes from user input
	- S22 : Front end design for user input on startup details.
	- S23 : Deploy flask app on which users interact with model.
	- S24 : Setup Amazon cloud server for file hosting.
- E9 - Interactive display for ""Choose your adventure"" story
	- S25 : Interactive interface to select geolocation of startup.
	- S26 : Interactive drop downs and valuation metrics upon toggling options.
	- S27 : Storyline for selecting startup options and journey.

## Backlog

- S1 : Cleaned data on general information for each startup. (1) - Sprint 1 (April 12 - April 26)
- S2 : New features based on funding frequencies, amounts, target market. (3) - Sprint 1 (April 12 - April 26)
- S3 : Cleaned data on venture rounds that were raised by startups during this  period. (2) - Sprint 1 (April 12 - April 26)
- S4 : New features based on the type of venture round that was raised - seed, growth etc. (3) - Sprint 1 (April 12 - April 26)
- S5 : Venture type and amount trends across time period. (3) - Sprint 1 (April 12 - April 26)
- S6 : Cleaned data on venture investors during time period. (2) - Sprint 1 (April 12 - April 26)
- S7 : Scoring of venture investors based on frequency, amount of fundings. (5)
- S9 : Cleaned data on mergers and acquisitions during this period. (2) - Sprint 1 (April 12 - April 26)
- S10 : New features based on how accretive acquisition was. (3) - Sprint 1 (April 12 - April 26)
- S12 : Acquired external data on macro trends during time period. (5)
- S13 : Cleaned data on external macro trends. (2)
- S15 : Grouped, aggregated, and in-depth EDA across all collected data. (3)
- S16 : New features from combined datasets. (5)
- S17 : Base logistic regression model for multilabel classification. (3)
- S18 : Model selection and model tuning for multilabel classification. (8)
- S19 : Base regression model for funding amounts. (3)
- S20 : Model selection and model tuning for regression model on funding amounts. (8)
- S22 : Front end design for user input on startup details. (8)
- S23 : Deploy flask app on which users interact with model. (8)
- S24 : Setup Amazon cloud server for file hosting. (8)

## Icebox

- S8 : Social media and online mention frequency and influence of venture capital investors. (13)
- S11 : Success metric and scoring to gauge venture outcome. (8)
- S14 : New features based on how macro trends compare across different time periods. (13)
- S21 : Estimate valuation of startup based on combination of predictive models. (21)
- S25 : Interactive interface to select geolocation of startup. (21)
- S26 : Interactive drop downs and valuation metrics upon toggling options. (21)
- S27 : Storyline for selecting startup options and journey. (21)
