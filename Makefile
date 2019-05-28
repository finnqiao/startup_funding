.PHONY: data

data/external/companies.csv: config/model_config.yml
	python src/ingest_data.py --config=config/model_config.yml --save=data/external/


data/auxiliary/new_companies_data.csv:
	python src/clean_companies_data.py --config=config/model_config.yml --input_file=data/external/companies.csv --save=data/auxiliary/new_companies_data.csv
