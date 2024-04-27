from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin(origin='*')
def index():
    return "Hello, World!"
@app.route('/create_auction', methods=['GET'])
@cross_origin(origin='*')
def create_auction():
    # Create a new connection within the request handler
    with sqlite3.connect('main.db') as con:
        cur = con.cursor()

        try:
            cur.execute("CREATE TABLE IF NOT EXISTS auctions(channel_link TEXT, description TEXT, min_bet_ton TEXT, create_data INTEGER, end_data INTEGER)")
        except Exception as e:
            print("Error creating table:", e)

        # Fetch data from the 'auctions' table
        cur.execute("SELECT * FROM auctions")
        rows = cur.fetchall()

        # Construct a list of dictionaries for each auction
        auctions = []
        for row in rows:
            auction = {
                "channel_link": row[0],
                "description": row[1],
                "min_bet_ton": row[2],
                "create_data": row[3],
                "end_data": row[4]
            }
            auctions.append(auction)

        # Return the list of auctions as JSON
        return jsonify({"data": auctions})

@app.route('/create_auction', methods=['DELETE'])
@cross_origin(origin='*')
def delete_auction():
    # Extract the channel ID from the request parameters
    channel_id = request.args.get('channel_id')

    if not channel_id:
        return jsonify({"error": "Channel ID not provided"}), 400

    # Create a new connection within the request handler
    with sqlite3.connect('main.db') as con:
        cur = con.cursor()

        # Delete rows from the 'auctions' table where the channel_link matches the provided channel ID
        cur.execute("DELETE FROM auctions WHERE channel_link = ?", (channel_id,))
        con.commit()

        return jsonify({"message": f"Auctions with channel ID {channel_id} have been deleted"})
