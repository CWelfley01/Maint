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


class MaintRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datein = db.Column(db.String, nullable=False)
    datestarted = db.Column(db.String, nullable=False)
    datecompleted = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    actiontaken = db.Column(db.String, nullable=False)
    tech = db.Column(db.String, nullable=False)
    

    def __init__(self, datein, datestarted, datecompleted, description, actiontaken, tech):
        self.datein = datein
        self.datestarted = datestarted
        self.datecompleted = datecompleted 
        self.description = description
        self.actiontaken = actiontaken
        self.tech = tech
        

class MaintRecordSchema(ma.Schema):
    class Meta:
        fields = ("id", "datein", "datestarted", "datecompleted", "description", "actiontaken", "tech")

maintrecord_schema = MaintRecordSchema()
maintrecords_schema = MaintRecordSchema(many=True)

@app.route("/add-record", methods=["POST"])
def add_record():
    datein = request.json.get("datein")
    datestarted = request.json.get("datestarted")
    datecompleted = request.json.get("datecompleted")
    description = request.json.get("description")
    actiontaken = request.json.get("actiontaken")
    tech = request.json.get("tech")
    

    record = MaintRecords(datein, datestarted, datecompleted, description, actiontaken, tech)
    
    db.session.add(record)
    db.session.commit()

    return jsonify(maintrecord_schema.dump(record))

@app.route("/maintrecords", methods=["GET"])
def get_all_maintrecords():
    all_maintrecords = maintrecords.query.all()
    return jsonify(maintrecords_schema.dump(all_maintrecords))

@app.route("/maintrecord/<id>", methods=["DELETE","GET","PUT"])
def maintrecord_id(id):
    maintrecord = MaintRecords.query.get(id)
    if request.method == "DELETE":
        db.session.delete(maintrecord)
        db.session.commit()
    
        return maintrecord_schema.jsonify(maintrecord)
    elif request.method == "PUT":
        datein = request.json['datein']
        datestarted = request.json['datestarted']
        datecompleted = request.json['datecompleted']
        description = request.json['description']
        actiontaken = request.json['actiontaken']
        tech = request.json['tech']
       

        maintrecord.datein = datein
        maintrecord.datestarted = datestarted
        maintrecord.datecompleted = datecompleted
        maintrecord.description = description
        maintrecord.actiontaken = actiontaken
        maintrecord.tech = tech

        db.session.commit()
        return maintrecord_schema.jsonify(maintrecord)
    elif request.method == "GET":
        return maintrecord_schema.jsonify(maintrecord)



if __name__ == "__main__":
    app.run(debug=True)
