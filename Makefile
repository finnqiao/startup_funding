.PHONY: data

data/external/companies.csv: config/model_config.yml
	python src/ingest_data.py --config=config/model_config.yml --save=data/external/

company_data: data/external/companies.csv

data/external/investments.csv: config/model_config.yml
	python src/ingest_data.py --config=config/model_config.yml --save=data/external/

investment_data: data/external/investments.csv

data/external/acquisitions.csv: config/model_config.yml
	python src/ingest_data.py --config=config/model_config.yml --save=data/external/

acquisition_data: data/external/acquisitions.csv

data/external/rounds.csv: config/model_config.yml
	python src/ingest_data.py --config=config/model_config.yml --save=data/external/

rounds_data: data/external/rounds.csv

data/external/ipo_counts.csv: config/model_config.yml
	python src/ingest_data.py --config=config/model_config.yml --save=data/external/

ipo_data: data/external/ipo_counts.csv

data: company_data investment_data acquisition_data rounds_data ipo_data

data/auxiliary/new_companies_data.csv: data/external/companies.csv
	python src/clean_companies_data.py --config=config/model_config.yml --input_file=data/external/companies.csv --save=data/auxiliary/new_companies_data.csv

clean_company: data/auxiliary/new_companies_data.csv

data/auxiliary/new_investors_data.csv: data/external/investments.csv
	python src/clean_investors_data.py --config=config/model_config.yml --input_file=data/external/investments.csv --save=data/auxiliary/new_investors_data.csv

clean_investments: data/auxiliary/new_investors_data.csv

data/auxiliary/new_acquisitions_data.csv: data/external/acquisitions.csv
	python src/clean_acquisitions_data.py --config=config/model_config.yml --input_file=data/external/acquisitions.csv --save=data/auxiliary/new_acquisitions_data.csv

clean_acquisitions: data/auxiliary/new_acquisitions_data.csv

data/auxiliary/new_rounds_data.csv: data/external/rounds.csv
	python src/clean_rounds_data.py --config=config/model_config.yml --input_file=data/external/rounds.csv --save=data/auxiliary/new_rounds_data.csv

clean_rounds: data/auxiliary/new_rounds_data.csv

data/auxiliary/new_ipo_data.csv: data/external/ipo_counts.csv
	python src/clean_macro_data.py --config=config/model_config.yml --input_file=data/external/ipo_counts.csv --save=data/auxiliary/new_ipo_data.csv

clean_ipo: data/auxiliary/new_ipo_data.csv

clean_data: clean_company clean_investments clean_acquisitions clean_rounds clean_ipo

data/auxiliary/aggregated_data.csv: data/auxiliary/new_companies_data.csv data/auxiliary/new_investors_data.csv data/auxiliary/new_acquisitions_data.csv data/auxiliary/new_rounds_data.csv data/auxiliary/new_ipo_data.csv
	python src/preprocess_merge_data.py --config=config/model_config.yml --save=data/auxiliary/aggregated_data.csv

merge_data: data/auxiliary/aggregated_data.csv

all: |data clean_data merge_data
