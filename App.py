import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify,g
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import sqlite3


engine = create_engine("sqlite:///Resources/hawaii.sqlite") 

#'borrowing' from code used in the earlier part of the assignment
Base = automap_base()
Base.prepare(engine, reflect=True)

# doing my best w/o being able to import anything.  Dont have high
# hopes, but we'll see

# Save references to table
Stations = Base.classes.station
session = Session(engine)
Measurements = Base.classes.measurement

app = Flask(__name__)

# Flask routes

@app.route("/")
def welcome():
    """List all routes that are available"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/:start_date<br/>"
        f"Please choose your starting and ending date between 2010-01-01 and 2017-08-23 for the following search<br/>"
        f"/api/v1.0/:start_date/:end_date"
    )

##########################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns precipitation data with corresponding dates"""
    previous_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    previous_yr_precip = session.query(Measurements.date,Measurements.prcp).filter\
        (Measurements.date >= previous_yr).order_by(Measurements.date).all()
    dictionary = [r._asdict() for r in previous_yr_precip]
    return jsonify(dictionary)

############################################################################

@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of stations from the dataset"""
    stations = session.qury(Stations.station).all()
    return jsonify(stations)

##############################################################################

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of Temperature Observations (tobs) from the previous year"""
    previous_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    previous_yr_tobs = session.query(Measurements.date,Measurements.tobs).filter\
        (Measurements.date >= previous_yr).order_by(Measurements.date).all()
    return jsonify(previous_yr_tobs)

##################################################################################

@app.route("/api/v1.0/<start_date")
def start_date(start_date):
    start_date = session.query(func.min(Measurements.tobs), func.avg\
        (Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= \
            start_date).all()
    for data in start_date:
        (tmin, tave, tmax) = data
        return jsonify(min_temp = tmin, ave_temp = tave, max_temp = tmax)

######################################################################################

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    start_end = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.\
        max(Measurements.tobs)).filter(Measurements.date >= start_date).filter(Measurements.\
            date <= end_date).all()
    for data in start_end:
        (tmin, tave, tmax) = data
        return jsonify(min_temp = tmin, ave_temp = tave, max_temp = tmax)

########################################################################################
 
if __name__ == "__main__":
    app.run(debug = True)