import os
import sys
import logging
import pandas as pd
import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql

import argparse

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger('sql_db')

Base = declarative_base()

class Funding_Prediction(Base):
    """Create a table to store predictions for average funding amount"""

    __tablename__ = 'funding_prediction'

    user_session_id = Column(String(500), primary_key=True, unique=True, nullable=False)
    user_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    predicted_amount = Column(Float, unique=False, nullable=False)

# class Company_Features(Base):
#     """
#     Create a table to store all the url data and generated features.
#     """
#
#     __tablename__ = 'url_features'
#
#     url = Column(String(500), primary_key=True, unique=True, nullable=False)
#     no_of_dots = Column(Integer, unique= False, nullable=False)
#     no_of_hyphen = Column(Integer, unique= False, nullable=False)
#     len_of_url = Column(Float, unique= False, nullable=False)
#     no_of_at = Column(Integer, unique= False, nullable=False)
#     no_of_double_slash = Column(Integer, unique= False, nullable=False)
#     no_of_subdir = Column(Integer, unique= False, nullable=False)
#     no_of__subdomain = Column(Integer, unique= False, nullable=False)
#     len_of_domain = Column(Integer, unique= False, nullable=False)
#     no_of_queries = Column(Integer, unique= False, nullable=False)
#     contains_IP = Column(Integer, unique= False, nullable=False)
#     presence_of_suspicious_TLD = Column(Integer, unique= False, nullable=False)
#     create_age = Column(Integer, unique= False, nullable=False)
#     expiry_age = Column(Integer, unique= False, nullable=False)
#     update_age = Column(Integer, unique= False, nullable=False)
#     country = Column(String(100), unique= False, nullable=False)
#     file_extension = Column(String(100), unique= False, nullable=False)
#     risk_indicator = Column(Integer, unique= False, nullable=False)
#     label = Column(Integer, unique= False, nullable=False)

def get_engine_string(RDS = False):
    """
    Get the engine string for RDS, get the path of sqlite database schema if RDS = False.
    Args:
    RDS(bool): Default False. If False: create the database schema locally in sqlite.
                              If True: create the database schema in RDS.
    Return:
    String: An engine_string if RDS = True
            Path to store sqlite database if RDS = False
    """
    if RDS:
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        DATABASE_NAME = 'startup_funding'
        engine_string = "{}://{}:{}@{}:{}/{}". \
            format(conn_type, user, password, host, port, DATABASE_NAME)
        logging.debug("engine string: %s"%engine_string)
        return  engine_string
    else:
        return 'sqlite:///startupfund.db'

def create_db(args,engine=None):
    """Creates a database with the data models inherited from `Base`"""
    if engine is None:
        RDS = eval(args.RDS)
        logger.info("RDS:%s"%RDS)
        engine = sql.create_engine(get_engine_string(RDS = RDS))

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logging.info("database created")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--RDS", default="False",help="True if want to create in RDS else None")
    args = parser.parse_args()

    engine = create_db(args)

    # create engine
    engine = sql.create_engine(get_engine_string(RDS=args.RDS))

    # create a db session
    Session = sessionmaker(bind=engine)
    session = Session()

    # insert a new url to prediction table for testing
    input_user = Funding_Prediction(user_session_id='aba124jd1', predicted_amount=34500.0)
    session.add(input_user)
    session.commit()

    logger.info("New user input added")

    # check if the new url was inserted successfully
    query = "SELECT * FROM funding_prediction"
    df = pd.read_sql(query, con=engine)
    logger.info(df)
