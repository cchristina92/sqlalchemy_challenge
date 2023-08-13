# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import and_, or_, not_
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()


# reflect the tables
Base.prepare(autoload_with = engine)

#Base.classes.keys()



# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



# #################################################
# # Flask Routes
# #################################################

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "<div><h1>Surfs Up!</h1><h3>Weclome to the Hawaiian climate API!</h3><h3>Here are the available routes</h3><p>/api/v1.0/precipitation</p><p>/api/v1.0/stations</p><p>/api/v1.0/tobs</p><p>/api/v1.0/[start]</p><p>/api/v1.0/[start]/[end]</p></div><div><h4>Note: when adding dates after /api/v1.0/ you must use the format <b>yyyy-mm-dd</b></h4></div>"


#Define what to do when a user hits the precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
  #  session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()
    precip = {date: prcp for date, prcp in results}
    return jsonify(precipitation=precip)
    

#Define what to do when a user hits the station route
@app.route("/api/v1.0/stations")
def stations():
   # session = Session(engine)
    data = session.query(Station.station, Station.name).all()
    session.close()
    stations = {station: name for station, name in data}
    return jsonify(stations=stations)
    

#Define what to do when a user hits the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
  #  session = Session(engine)
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    data = session.query(Measurement.tobs, Measurement.date).filter(and_(Measurement.station == 'USC00519281'), (Measurement.date >= prev_year)).all()
    session.close()
    tobs = {date: tobs for date, tobs in data}
    return jsonify(tobs=tobs)
    

#Define what to do when a user adds a start and end date
@app.route("/api/v1.0/<start>/<end>")
def startEndPath(start, end):
    #session = Session(engine)
    data = session.query( func.min(Measurement.tobs), func.max(Measurement.tobs),  func.avg(Measurement.tobs)).filter(and_(Measurement.date >= start, Measurement.date <= end )).all()
    session.close()
    tobs = list(np.ravel(data))
    return jsonify(temperature=tobs)
    

#Define what to do when a user adds just a start date
@app.route("/api/v1.0/<start>")
def startPath(start):
    #session = Session(engine)
    data = session.query( func.min(Measurement.tobs), func.max(Measurement.tobs),  func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    tobs = list(np.ravel(data))
    return jsonify(temperature=tobs)
   


if __name__ == "__main__":
    app.run(debug=True)