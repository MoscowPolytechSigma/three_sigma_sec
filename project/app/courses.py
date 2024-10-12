from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from models import db, User, Building, Room, Department
from sqlalchemy import desc, func
from math import ceil

bp = Blueprint('courses', __name__, url_prefix='/courses')

COURSE_PARAMS = [
    'author_id', 'name', 'category_id', 'short_desc', 'full_desc'
]

def params():
    return { p: request.form.get(p) or None for p in COURSE_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': [x for x in request.args.getlist('category_ids') if x],
    }

@bp.route('/')
def index():
    return render_template('index.html')

# Function to calculate areas and volumes
@bp.route('/calculate', methods=['GET'])
def calculate():
    rooms = db.session.execute(db.select(Room)).scalars().all()  # Fixed query call
    results = []
    for room in rooms:
        area = room.width * room.length
        volume = area * room.building.ceiling_height
        results.append({
            'room_number': room.room_number,
            'area': area,
            'volume': volume
        })
    return render_template('courses/calculate_results.html', results=results)

# Get departments in a building
@bp.route('/departments/<int:building_id>', methods=['GET', 'POST'])
def get_departments(building_id):
    departments = Department.query.join(Room).filter(Room.building_id == building_id).all()
    return render_template('departments.html', departments=[dept.name for dept in departments])

# Add a new building
@bp.route('/buildings', methods=['GET', 'POST'])
def add_building():
    if request.method == 'POST':
        name = request.form.get('name')
        ceiling_height = float(request.form.get('ceiling_height'))
        
        if not name or not ceiling_height:
            return render_template('error.html', message='Invalid input'), 400  # Handle missing input
        
        new_building = Building( name=name, ceiling_height=ceiling_height)
        db.session.add(new_building)
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to index after adding
    
    return render_template('courses/add_building.html')  # Render form for adding a building

@bp.route('/show_building', methods=['GET'])
def show_building():
    return render_template('courses/list_of_buildings.html', building = Building)  # Render form for adding a building


# Update building information
@bp.route('/buildings/<int:id>', methods=['GET', 'POST'])
def update_building(id):
    building = Building.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        ceiling_height = request.form.get('ceiling_height')
        
        if not name or not ceiling_height:
            return render_template('error.html', message='Invalid input'), 400  # Handle missing input
        
        building.name = name
        building.ceiling_height = ceiling_height
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to index after updating

    return render_template('courses/update_building.html', building=building)  # Render form for updating a building

# Add a new room
@bp.route('/rooms', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        building_id = request.form.get('building_id')
        room_number = request.form.get('room_number')
        location = request.form.get('location')
        width = request.form.get('width')
        length = request.form.get('length')
        purpose = request.form.get('purpose')
        type_ = request.form.get('type')
        department_id = request.form.get('department_id')

        if not all([building_id, room_number, location, width, length, purpose, type_]):
            return render_template('error.html', message='Invalid input'), 400  # Handle missing input
        
        new_room = Room(
            building_id=building_id,
            room_number=room_number,
            location=location,
            width=width,
            length=length,
            purpose=purpose,
            type=type_,
            department_id=department_id
        )
        
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to index after adding

    return render_template('courses/add_room.html')  # Render form for adding a room

# Update room information
@bp.route('/rooms/<int:id>', methods=['GET', 'POST'])
def update_room(id):
    room = Room.query.get_or_404(id)

    if request.method == 'POST':
        room_number = request.form.get('room_number')
        location = request.form.get('location')
        width = request.form.get('width')
        length = request.form.get('length')
        purpose = request.form.get('purpose')
        type_ = request.form.get('type')
        
        if not all([room_number, location, width, length, purpose, type_]):
            return render_template('error.html', message='Invalid input'), 400  # Handle missing input
        
        room.room_number = room_number
        room.location = location
        room.width = width
        room.length = length
        room.purpose = purpose
        room.type = type_
        
        department_id = request.form.get('department_id')
        
        if department_id:
            room.department_id = department_id

        db.session.commit()
        return redirect(url_for('index'))  # Redirect to index after updating

    return render_template('courses/update_room.html', room=room)  # Render form for updating a room