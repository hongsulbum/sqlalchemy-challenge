from flask import Flask, jsonify, escape

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import timedelta


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
        return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/{escape('<start>')} (please enter start date in the following format: YYYY-MM-DD)<br/>"
        f"/api/v1.0/{escape('<start>')}/{escape('<end>')}<br/> (please enter start and end dates in the following format: YYYY-MM-DD)"        
        )

@app.route("/api/v1.0/precipitation")
def precip():
        session = Session(engine)

        results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= dt.date(2016, 8, 23)).all()

        session.close()

        precip_data = {}

        for result in results:
                if result[0] not in precip_data:
                        precip_data[result[0]] = []
                        precip_data[result[0]].append(result[1])
                else:
                        precip_data[result[0]].append(result[1])
        
        return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def station():
        session = Session(engine)
        station_results = session.query(Measurement.station).all()
        session.close()

        stations_list = []

        for result in station_results:
                if result[0] not in stations_list:
                        stations_list.append(result[0])

        return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
        session = Session(engine)

        temp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= dt.date(2016, 8, 23)).all()

        session.close()

        return jsonify(temp_results)

@app.route("/api/v1.0/<start>")
def min_avg_max_start(start):
        session = Session(engine)

        results = session.query(Measurement.tobs).filter(Measurement.date >= start).all()

        temps_in_range = []

        for result in results:
                temps_in_range.append(result[0])
        
        min_temp = min(temps_in_range)
        avg_temp = (sum(temps_in_range) / len(temps_in_range))
        max_temp = max(temps_in_range)

        return f"From the date starting {start} through 2017-08-23, <br/> the minimum recorded temperature was {min_temp}, <br/> the average recorded temperature was {avg_temp:.01f}, <br/> and the maximum recorded temperature was {max_temp}."

@app.route("/api/v1.0/<start>/<end>")
def min_avg_max_start_end(start, end):
        session = Session(engine)

        results = session.query(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

        temps_in_range = []

        for result in results:
                temps_in_range.append(result[0])

        min_temp = min(temps_in_range)
        avg_temp = (sum(temps_in_range) / len(temps_in_range))
        max_temp = max(temps_in_range)

        return f"From the date starting {start} through {end}, <br/> the minimum recorded temperature was {min_temp}, <br/> the average recorded temperature was {avg_temp:.01f}, <br/> and the maximum recorded temperature was {max_temp}."

if __name__ == "__main__":
    app.run(debug=True)