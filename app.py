from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from main import *
import json, codecs
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///droneflymap.db'
db = SQLAlchemy(app)

class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Double(30), nullable=False)
    longitude = db.Column(db.Double(30), nullable=False)

    def __repr__(self):
        return '<Target %r>' % self.id

class Takeoff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    takeoff_latitude = db.Column(db.Double(30), nullable=False)
    takeoff_longitude = db.Column(db.Double(30), nullable=False)

    def __repr__(self):
        return '<Takeoff %r>' % self.id

class Landing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    landing_latitude = db.Column(db.Double(30), nullable=False)
    landing_longitude = db.Column(db.Double(30), nullable=False)

    def __repr__(self):
        return '<Landing %r>' % self.id

class Drone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_flight_time = db.Column(db.Integer, nullable=False)
    average_speed = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Drone %r>' % self.id

@app.route('/')
def index():
    targets = Target.query.order_by(Target.id).all()
    takeoffs = Takeoff.query.order_by(Takeoff.id).all()
    landings = Landing.query.order_by(Landing.id).all()
    drones = Drone.query.order_by(Drone.id).all()
    return render_template('index.html', targets=targets, drones=drones,
                           takeoffs=takeoffs, landings=landings)

#---- Upload File -----
@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        contents = file.readlines()
        points_coordinate = np.array([np.asfarray(contents[5].split(b' '))])
        new_drone = Drone(average_speed=float(contents[1]), max_flight_time=float(contents[0]))
        takeoff = np.asfarray(contents[2].split(b' '))
        new_takeoff = Takeoff(takeoff_latitude=float(takeoff[0]), takeoff_longitude=float(takeoff[1]))
        landing = np.asfarray(contents[3].split(b' '))
        new_landing = Landing(landing_latitude=float(landing[0]), landing_longitude=float(landing[1]))
        num_points = int(contents[4])-1
        for i in range(num_points):
            points_coordinate = np.append(points_coordinate, np.array([np.asfarray(contents[6 + i].split(b' '))]),
                                          axis=0)
        try:
            db.session.add(new_drone)
            db.session.add(new_takeoff)
            db.session.add(new_landing)
            for target in points_coordinate:
                db.session.add(Target(latitude=float(target[0]), longitude=float(target[1])))
            db.session.commit()
            return redirect('/')

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        return 'No file uploaded'

#---- Map Rules -----
@app.route('/map_get_targets')
def map_get_targets():
    targets = Target.query.order_by(Target.id).all()
    targets_list = [{'id': target.id, 'lat': target.latitude, 'lng': target.longitude} for target in targets]
    return jsonify(targets_list)

@app.route('/map_get_takeoffs')
def map_get_takeoffs():
    takeoffs = Takeoff.query.order_by(Takeoff.id).all()
    takeoffs_list = [{'lat': takeoff.takeoff_latitude, 'lng': takeoff.takeoff_longitude} for takeoff in takeoffs]
    return jsonify(takeoffs_list)

@app.route('/map_get_landings')
def map_get_landings():
    landings = Landing.query.order_by(Landing.id).all()
    landings_list = [{'lat': landing.landing_latitude, 'lng': landing.landing_longitude} for landing in landings]
    return jsonify(landings_list)

@app.route('/map_add_target', methods=['POST'])
def map_add_target():
    if request.method == 'POST':
        target_latitude = request.json.get('latitude')
        target_longitude = request.json.get('longitude')
        new_target = Target(latitude=target_latitude, longitude=target_longitude)

        try:
            db.session.add(new_target)
            db.session.commit()
            # return jsonify(redirect(url_for('index')))  # Redirect to the home route
            # redirect('/')
            return jsonify({'message': 'Target added successfully'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Add route to handle deletion of targets from the database
@app.route('/map_delete_target', methods=['POST'])
def map_delete_target():
    if request.method == 'POST':
        target_latitude = request.json.get('latitude')
        target_longitude = request.json.get('longitude')

        # Find the target with matching latitude and longitude
        target = Target.query.filter_by(latitude=target_latitude, longitude=target_longitude).first()

        if target:
            # Delete the target from the database
            db.session.delete(target)
            db.session.commit()
            return jsonify({'message': 'Target deleted successfully'})
        else:
            return jsonify({'error': 'Target not found'}), 404

@app.route('/map_add_takeoff', methods=['POST'])
def map_add_takeoff():
    if request.method == 'POST':
        takeoff_latitude = request.json.get('latitude')
        takeoff_longitude = request.json.get('longitude')
        new_takeoff = Takeoff(takeoff_latitude=takeoff_latitude, takeoff_longitude=takeoff_longitude)

        try:
            db.session.add(new_takeoff)
            db.session.commit()
            return jsonify({'message': 'Takeoff added successfully'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/map_delete_takeoff', methods=['POST'])
def map_delete_takeoff():
    if request.method == 'POST':
        takeoff_latitude = request.json.get('latitude')
        takeoff_longitude = request.json.get('longitude')

        # Find the takeoff with matching latitude and longitude
        takeoff = Takeoff.query.filter_by(takeoff_latitude=takeoff_latitude, takeoff_longitude=takeoff_longitude).first()

        if takeoff:
            # Delete the takeoff from the database
            db.session.delete(takeoff)
            db.session.commit()
            return jsonify({'message': 'Takeoff deleted successfully'})
        else:
            return jsonify({'error': 'Takeoff not found'}), 404

@app.route('/map_add_landing', methods=['POST'])
def map_add_landing():
    if request.method == 'POST':
        landing_latitude = request.json.get('latitude')
        landing_longitude = request.json.get('longitude')
        new_landing = Landing(landing_latitude=landing_latitude, landing_longitude=landing_longitude)

        try:
            db.session.add(new_landing)
            db.session.commit()
            return jsonify({'message': 'Landing added successfully'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/map_delete_landing', methods=['POST'])
def map_delete_landing():
    if request.method == 'POST':
        landing_latitude = request.json.get('latitude')
        landing_longitude = request.json.get('longitude')

        # Find the landing with matching latitude and longitude
        landing = Landing.query.filter_by(landing_latitude=landing_latitude, landing_longitude=landing_longitude).first()

        if landing:
            # Delete the landing from the database
            db.session.delete(landing)
            db.session.commit()
            return jsonify({'message': 'Landing deleted successfully'})
        else:
            return jsonify({'error': 'Landing not found'}), 404

#---- Target Rules -----
@app.route('/add_target', methods=['POST','GET'])
def add_target():
    target_latitude = request.form['latitude']
    target_longitude = request.form['longitude']
    new_target = Target(latitude=target_latitude, longitude=target_longitude)

    try:
        db.session.add(new_target)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was am issue adding target'

@app.route('/delete_target/<int:id>')
def delete_target(id):
    target_to_delete=Target.query.get_or_404(id)

    try:
        db.session.delete(target_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is a issue with deleting target'

@app.route('/update_target/<int:id>', methods=['POST','GET'])
def update_target(id):
    target = Target.query.get_or_404(id)

    if request.method == 'POST':
        target.latitude = request.form['latitude']
        target.longitude = request.form['longitude']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating target'

    else:
        return render_template('update.html', target=target)

@app.route('/add_takeoff', methods=['POST','GET'])
def add_takeoff():
    takeoff_latitude = request.form['latitude']
    takeoff_longitude = request.form['longitude']
    new_takeoff = Takeoff(takeoff_latitude=takeoff_latitude, takeoff_longitude=takeoff_longitude)

    try:
        db.session.add(new_takeoff)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was am issue adding takeoff point'

@app.route('/delete_takeoff/<int:id>')
def delete_takeoff(id):
    takeoff_to_delete=Takeoff.query.get_or_404(id)

    try:
        db.session.delete(takeoff_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is a issue with deleting takeoff point'

@app.route('/update_takeoff/<int:id>', methods=['POST','GET'])
def update_takeoff(id):
    takeoff = Takeoff.query.get_or_404(id)

    if request.method == 'POST':
        takeoff.takeoff_latitude = request.form['latitude']
        takeoff.takeoff_longitude = request.form['longitude']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating takeoff point'

    else:
        return render_template('update_takeoff.html', takeoff=takeoff)

@app.route('/add_landing', methods=['POST','GET'])
def add_landing():
    landing_latitude = request.form['latitude']
    landing_longitude = request.form['longitude']
    new_landing = Landing(landing_latitude=landing_latitude, landing_longitude=landing_longitude)

    try:
        db.session.add(new_landing)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was am issue adding landing point'

@app.route('/delete_landing/<int:id>')
def delete_landing(id):
    landing_to_delete=Landing.query.get_or_404(id)

    try:
        db.session.delete(landing_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is a issue with deleting landing point'

@app.route('/update_landing/<int:id>', methods=['POST','GET'])
def update_landing(id):
    landing = Landing.query.get_or_404(id)

    if request.method == 'POST':
        landing.landing_latitude = request.form['latitude']
        landing.landing_longitude = request.form['longitude']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating landing point'

    else:
        return render_template('update_landing.html', landing=landing)

#----- Drone Rules ------
@app.route('/add_drone', methods=['POST','GET'])
def add_drone():
    drone_speed = request.form['speed']
    drone_timetofly = request.form['timetofly']
    new_drone = Drone(average_speed=drone_speed, max_flight_time=drone_timetofly)

    try:
        db.session.add(new_drone)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was am issue adding drone'

@app.route('/delete_drone/<int:id>')
def delete_drone(id):
    drone_to_delete=Drone.query.get_or_404(id)

    try:
        db.session.delete(drone_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is a issue with deleting target'

@app.route('/update_drone/<int:id>', methods=['POST','GET'])
def update_drone(id):
    drone = Drone.query.get_or_404(id)

    if request.method == 'POST':
        drone.average_speed = request.form['speed']
        drone.max_flight_time = request.form['timetofly']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating drone'

    else:
        return render_template('update_drone.html', drone=drone)

def get_targets():
    return Target.query.all()

def get_takeoff():
    takeoff = Takeoff.query.all()
    return [takeoff[0].takeoff_latitude, takeoff[0].takeoff_longitude]

def get_landing():
    landing = Landing.query.all()
    return [landing[0].landing_latitude, landing[0].landing_longitude]

def get_drones():
    drone = Drone.query.all()
    return [drone[0].max_flight_time,drone[0].average_speed]

# def process_targets(targets):
#     return [[target.latitude, target.longitude] for target in targets]

@app.route('/find_route')
def route_search():
    coordinate_targets = []
    coordinate_targets.append(get_takeoff())

    targets = get_targets()
    # coordinate_targets.append(([target.latitude, target.longitude] for target in targets))
    for i in range(len(targets)):
        coordinate_targets.append([targets[i].latitude, targets[i].longitude])
    coordinate_targets.append(get_landing())
    coordinate_targets = np.array(coordinate_targets)

    drones = get_drones()

    points_array, flight_distance, visited_num, speed, figure = find_route(2, coordinate_targets, drones)
    # output = io.BytesIO()
    # FigureCanvas(figure).print_png(output)
    # return Response(output.getvalue(), mimetype='image/png')

    id_route = []
    for targets_coordinate in points_array:
        target = Target.query.filter_by(latitude=targets_coordinate[0], longitude=targets_coordinate[1]).first()
        if target:
            id_route.append(target.id)

    points_array = points_array.tolist()
    points_list = [{'lat': point[0], 'lng': point[1]} for point in points_array]
    return render_template('result_route.html', id_route=id_route, points_array=points_list,
                           flight_distance=round(flight_distance,2), time=round(flight_distance/speed*60,2), num_points=len(targets), visited_num=visited_num-2)

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
