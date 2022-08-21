from pydoc import describe
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

# maint table

class MaintRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datein = db.Column(db.String, nullable=False)
    started = db.Column(db.String, nullable=False)
    completed = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    actiontaken = db.Column(db.String, nullable=False)
    tech = db.Column(db.String, nullable=False)
    

    def __init__(self, datein, started, completed, description, actiontaken, tech):
        self.datein = datein
        self.started = started
        self.completed = completed 
        self.description = description
        self.actiontaken = actiontaken
        self.tech = tech
        

class MaintRecordSchema(ma.Schema):
    class Meta:
        fields = ("id", "datein", "started", "completed", "description", "actiontaken", "tech")

maintrecord_schema = MaintRecordSchema()
maintrecords_schema = MaintRecordSchema(many=True)

# forklift table

class ForkliftRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    serial = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    fuel = db.Column(db.String, nullable=False)
    engine = db.Column(db.String, nullable=False)
    

    def __init__(self, designation, model, serial, nickname, fuel, engine):
        self.designation = designation
        self.model = model
        self.serial = serial 
        self.nickname = nickname
        self.fuel = fuel
        self.engine = engine
        

class ForkliftRecordSchema(ma.Schema):
    class Meta:
        fields = ("id", "designation", "model", "serial", "nickname", "fuel", "engine")

forkliftrecord_schema = ForkliftRecordSchema()
forkliftrecords_schema = ForkliftRecordSchema(many=True)


# routes

@app.route("/add-maintrecord", methods=["POST"])
def add_maintrecord():
    datein = request.json.get("datein")
    started = request.json.get("started")
    completed = request.json.get("completed")
    description = request.json.get("description")
    actiontaken = request.json.get("actiontaken")
    tech = request.json.get("tech")
    

    record = MaintRecords(designation, model, serial, description, actiontaken, tech)
    
    db.session.add(record)
    db.session.commit()

    return jsonify(maintrecord_schema.dump(record))

@app.route("/add-forkliftrecord", methods=["POST"])
def add_forkliftrecord():
    designation = request.json.get("designation")
    model = request.json.get("model")
    serial = request.json.get("serial")
    nickname = request.json.get("nickname")
    fuel = request.json.get("fuel")
    engine = request.json.get("engine")
    

    record = MaintRecords(designation, model, serial, nickname, fuel, engine)
    
    db.session.add(record)
    db.session.commit()

    return jsonify(forkliftrecord_schema.dump(record))

@app.route("/maintrecords", methods=["GET"])
def get_all_maintrecords():
    all_maintrecords = maintrecords.query.all()
    return jsonify(maintrecords_schema.dump(all_maintrecords))

@app.route("/forkliftrecords", methods=["GET"])
def get_all_forkliftrecords():
    all_forkliftrecords = forkliftrecords.query.all()
    return jsonify(forkliftrecords_schema.dump(all_forkliftrecords))

@app.route("/maintrecord/<id>", methods=["DELETE","GET","PUT"])
def maintrecord_id(id):
    maintrecord = MaintRecords.query.get(id)
    if request.method == "DELETE":
        db.session.delete(maintrecord)
        db.session.commit()
    
        return maintrecord_schema.jsonify(maintrecord)
    elif request.method == "PUT":
        datein = request.json['datein']
        started = request.json['started']
        completed = request.json['completed']
        description = request.json['description']
        actiontaken = request.json['actiontaken']
        tech = request.json['tech']
       

        maintrecord.datein = datein
        maintrecord.started = started
        maintrecord.completed = completed
        maintrecord.description = description
        maintrecord.actiontaken = actiontaken
        maintrecord.tech = tech

        db.session.commit()
        return maintrecord_schema.jsonify(maintrecord)
    elif request.method == "GET":
        return maintrecord_schema.jsonify(maintrecord)
    
@app.route("/forkliftrecord/<id>", methods=["DELETE","GET","PUT"])
def forkliftrecord_id(id):
    forkliftrecord = ForkliftRecords.query.get(id)
    if request.method == "DELETE":
        db.session.delete(Forklikftrecord)
        db.session.commit()
    
        return forkliftrecord_schema.jsonify(forkliftrecord)
    elif request.method == "PUT":
        designation = request.json['designation']
        model = request.json['model']
        serial = request.json['serial']
        nickname = request.json['nickname']
        fuel = request.json['fuel']
        engine = request.json['engine']
       

        forkliftrecord.designation = designation
        forkliftrecord.model = model
        forkliftrecord.serial = serial
        forkliftrecord.nickname = nickname
        forkliftrecord.fuel = fuel
        forkliftrecord.engine = engine

        db.session.commit()
        return forkliftrecord_schema.jsonify(forkliftrecord)
    elif request.method == "GET":
        return forkliftrecord_schema.jsonify(forkliftrecord)



if __name__ == "__main__":
    app.run(debug=True)
