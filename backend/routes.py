from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Returns the loaded list containing all picture elements"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Finds and returns a single picture dictionary element matching the ID"""
    # Look for a picture where the integer id matches the item's id
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return jsonify({"message": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Creates a new picture entry and appends it to data"""
    new_picture = request.get_json()
    if not new_picture:
        return jsonify({"message": "Invalid or missing input data"}), 400
        
    # Check if a picture with this id already exists to avoid duplicates
    existing = next((item for item in data if item["id"] == new_picture.get("id")), None)
    if existing:
        # FIXED: Exact string and casing matching the test requirement
        return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    data.append(new_picture)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Updates an existing picture matching the provided id parameter"""
    update_data = request.get_json()
    if not update_data:
        return jsonify({"message": "Invalid or missing input data"}), 400

    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return jsonify({"message": "Picture not found"}), 404

    # Update the keys in-place
    picture.update(update_data)
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Deletes an item from the collection by its ID value"""
    global data
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return jsonify({"message": "Picture not found"}), 404

    # Remove the matching picture object from the list structure
    data = [item for item in data if item["id"] != id]
    
    # FIXED: Returns an empty response with a 204 status code as expected by the test
    return "", 204