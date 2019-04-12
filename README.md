# Startup Success Metrics for Venture Capital Firms

* [Product Charter](#product-charter)
	* [Mission](#mission)
	* [Vision](#vision)
	* [Success Criteria](#success-criteria)
* [Planned Work](#planned-work)
* [Backlog](#backlog)
* [Icebox](#icebox)

Scenario analysis of venture capital outcomes based on startup characteristics, funding history, and macroeconomic conditions.

## Product Charter

Primary focus of the app is to inform startups and venture capital funds alike on different startup success metrics like exit probabilities and funding amounts.

### Vision

Improve risk management by venture capital firms and fundraising decisions by startups.

### Mission

Utilize past venture outcomes to predict startup success on a variety of metrics like fundraising and exit opportunities.

### Success Criteria

An outcome accuracy of at least 65% for startup outcome classification.

Inbound traffic from 100 existing venture capital firms.

## Planned Work

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

- S1 : Cleaned data on general information for each startup. (1)
- S2 : New features based on funding frequencies, amounts, target market. (3)
- S3 : Cleaned data on venture rounds that were raised by startups during this  period. (2)
- S4 : New features based on the type of venture round that was raised - seed, growth etc. (3)
- S5 : Venture type and amount trends across time period. (3)
- S6 : Cleaned data on venture investors during time period. (2)
- S7 : Scoring of venture investors based on frequency, amount of fundings. (5)
- S9 : Cleaned data on mergers and acquisitions during this period. (2)
- S10 : New features based on how accretive acquisition was. (3)
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
