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

# Функция для расчета площадей и объемов
@bp.route('/calculate', methods=['GET'])
def calculate():
    rooms =  db.session.execute(db.select(Room)).scalars().all()
    results = []
    for room in rooms:
        area = room.width * room.length
        volume = area * room.building.ceiling_height
        results.append({
            'room_number': room.room_number,
            'area': area,
            'volume': volume
        })
    return jsonify(results)

# Получение информации о факультетах в корпусе
@bp.route('/departments/<int:building_id>', methods=['GET', 'POST'])
def get_departments(building_id):
    departments = Department.query.join(Room).filter(Room.building_id == building_id).all()
    return jsonify([dept.name for dept in departments])

# Добавление нового корпуса
@bp.route('/buildings', methods=['GET','POST'])
def add_building():
    data = request.json
    new_building = Building(name=data['name'], ceiling_height=data['ceiling_height'])
    db.session.add(new_building)
    db.session.commit()
    return jsonify({'message': 'Building added!'}), 201

# Изменение информации о корпусе
@bp.route('/buildings/<int:id>', methods=['PUT'])
def update_building(id):
    data = request.json
    building = Building.query.get_or_404(id)
    building.name = data['name']
    building.ceiling_height = data['ceiling_height']
    db.session.commit()
    return jsonify({'message': 'Building updated!'})

# Добавление нового помещения
@bp.route('/rooms', methods=['GET','POST'])
def add_room():
    data = request.json
    new_room = Room(
        building_id=data['building_id'],
        room_number=data['room_number'],
        location=data['location'],
        width=data['width'],
        length=data['length'],
        purpose=data['purpose'],
        type=data['type'],
        department_id=data.get('department_id')
    )
    db.session.add(new_room)
    db.session.commit()
    return jsonify({'message': 'Room added!'}), 201

# Изменение информации о комнате
@bp.route('/rooms/<int:id>', methods=['PUT'])
def update_room(id):
    data = request.json
    room = Room.query.get_or_404(id)
    room.room_number = data['room_number']
    room.location = data['location']
    room.width = data['width']
    room.length = data['length']
    room.purpose = data['purpose']
    room.type = data['type']
    
    if 'department_id' in data:
        room.department_id = data['department_id']

    db.session.commit()
    return jsonify({'message': 'Room updated!'})

