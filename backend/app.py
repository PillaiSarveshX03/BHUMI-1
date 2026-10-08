import os
import json
import sqlite3
from flask import Flask, request, jsonify, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE = 'bhumi.db'

def get_db():
    """Get database connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database and seed it with data if empty."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS districts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                data TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                district TEXT NOT NULL,
                data TEXT NOT NULL,
                UNIQUE(name, district)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Seed from Data/crops.json if crops table is empty
        cursor.execute('SELECT COUNT(*) as count FROM crops')
        if cursor.fetchone()['count'] == 0:
            json_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'crops.json')
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    seed_data = json.load(f)
                    districts = seed_data.get('regional_crop_agronomy_database', {}).get('districts', [])
                    if not districts:
                        districts = seed_data.get('districts', [])
                    
                    for d in districts:
                        # Insert district
                        d_copy = d.copy()
                        d_copy.pop('viable_recommended_crops', None)
                        cursor.execute('INSERT OR IGNORE INTO districts (name, data) VALUES (?, ?)', 
                                       (d['district_name'], json.dumps(d_copy)))
                        
                        # Insert crops
                        for crop in d.get('viable_recommended_crops', []):
                            cursor.execute('INSERT OR IGNORE INTO crops (name, district, data) VALUES (?, ?, ?)',
                                           (crop['crop_name'], d['district_name'], json.dumps(crop)))
                db.commit()
                print("Database seeded successfully.")
            except Exception as e:
                print(f"Error seeding database: {e}")

# Call init_db() on startup
with app.app_context():
    init_db()

@app.route('/api/crops', methods=['GET'])
def get_crops():
    """Get all crops (with optional filters) and all districts."""
    search = request.args.get('search', '').lower()
    region = request.args.get('region', '').lower()
    season = request.args.get('season', '').lower()
    soil = request.args.get('soil', '').lower()
    
    db = get_db()
    
    # Fetch districts
    districts = []
    for row in db.execute('SELECT data FROM districts'):
        districts.append(json.loads(row['data']))
        
    # Fetch crops
    crops = []
    for row in db.execute('SELECT id, district, data FROM crops'):
        crop_data = json.loads(row['data'])
        crop_data['id'] = row['id']
        crop_data['districtName'] = row['district']
        
        # Apply filters in Python
        if search and search not in crop_data.get('crop_name', '').lower() and \
           search not in crop_data.get('scientific_name', '').lower() and \
           search not in crop_data.get('growing_season', '').lower() and \
           search not in crop_data.get('target_soil_type', '').lower() and \
           search not in crop_data.get('districtName', '').lower():
            continue
            
        if region and region not in crop_data.get('districtName', '').lower():
            continue
            
        if season and season not in crop_data.get('growing_season', '').lower():
            continue
            
        if soil and soil not in crop_data.get('target_soil_type', '').lower():
            continue
            
        crops.append(crop_data)
        
    return jsonify({"districts": districts, "crops": crops})

@app.route('/api/crops/<int:id>', methods=['GET'])
def get_crop(id):
    """Get a specific crop by ID."""
    db = get_db()
    row = db.execute('SELECT district, data FROM crops WHERE id = ?', (id,)).fetchone()
    if row:
        crop_data = json.loads(row['data'])
        crop_data['id'] = id
        crop_data['districtName'] = row['district']
        return jsonify(crop_data)
    return jsonify({"error": "Crop not found"}), 404

@app.route('/api/crops', methods=['POST'])
def add_crop():
    """Add a new crop."""
    data = request.json
    if not data or 'crop_name' not in data or 'districtName' not in data:
        return jsonify({"error": "crop_name and districtName are required"}), 400
        
    db = get_db()
    try:
        db.execute('INSERT INTO crops (name, district, data) VALUES (?, ?, ?)',
                   (data['crop_name'], data['districtName'], json.dumps(data)))
        db.commit()
        return jsonify({"message": "Crop added successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Crop already exists in this district"}), 409

@app.route('/api/recommend', methods=['GET', 'POST'])
def recommend_crops():
    """Rule-based scoring for crop recommendation."""
    if request.method == 'GET':
        data = request.args
        if not data:
            return jsonify({
                "message": "Send a POST request with JSON payload or use GET with query parameters to get recommendations.",
                "example_usage_post": {"soil": "loam", "season": "kharif", "region": "sangli"},
                "example_usage_get": "/api/recommend?soil=loam&season=kharif&region=sangli"
            })
    else:
        data = request.json or {}
        
    req_soil = data.get('soil', '').lower()
    req_season = data.get('season', '').lower()
    req_region = data.get('region', '').lower()
    
    db = get_db()
    scored_crops = []
    
    for row in db.execute('SELECT id, district, data FROM crops'):
        crop_data = json.loads(row['data'])
        crop_data['id'] = row['id']
        crop_data['districtName'] = row['district']
        
        score = 0
        if req_soil and req_soil in crop_data.get('target_soil_type', '').lower():
            score += 1
        if req_season and req_season in crop_data.get('growing_season', '').lower():
            score += 1
        if req_region and req_region in crop_data.get('districtName', '').lower():
            score += 1
            
        # Only include if there's at least some match
        if score > 0:
            scored_crops.append({"score": score, "crop": crop_data})
            
    # Sort by score descending
    scored_crops.sort(key=lambda x: x['score'], reverse=True)
    
    # Return top 5
    top_5 = [item['crop'] for item in scored_crops[:5]]
    return jsonify(top_5)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get some basic stats (e.g. crop count per district)."""
    db = get_db()
    stats = {}
    total_crops = 0
    for row in db.execute('SELECT district, COUNT(*) as count FROM crops GROUP BY district'):
        stats[row['district']] = row['count']
        total_crops += row['count']
        
    return jsonify({
        "total_crops": total_crops,
        "district_breakdown": stats
    })

@app.route('/api/contact', methods=['POST'])
def save_contact():
    """Save contact form submission."""
    data = request.json
    if not data or not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({"error": "Name, email, and message are required"}), 400
        
    db = get_db()
    db.execute('''
        INSERT INTO messages (name, email, subject, message)
        VALUES (?, ?, ?, ?)
    ''', (data['name'], data['email'], data.get('subject', ''), data['message']))
    db.commit()
    
    return jsonify({"message": "Message received successfully."}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
