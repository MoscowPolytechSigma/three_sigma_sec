from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from models import db, Course, Category, User, Review
from tools import CoursesFilter, ImageSaver
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
    courses = CoursesFilter(**search_params()).perform()
    pagination = db.paginate(courses)
    courses = pagination.items
    categories = db.session.execute(db.select(Category)).scalars()
    return render_template('courses/index.html',
                           courses=courses,
                           categories=categories,
                           pagination=pagination,
                           search_params=search_params())

@bp.route('/new')
@login_required
def new():
    course = Course()
    categories = db.session.execute(db.select(Category)).scalars()
    users = db.session.execute(db.select(User)).scalars()
    return render_template('courses/new.html',
                           categories=categories,
                           users=users,
                           course=course)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    f = request.files.get('background_img')
    img = None
    course = Course()
    try:
        if f and f.filename:
            img = ImageSaver(f).save()

        image_id = img.id if img else None
        course = Course(**params(), background_image_id=image_id)
        db.session.add(course)
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        categories = db.session.execute(db.select(Category)).scalars()
        users = db.session.execute(db.select(User)).scalars()
        return render_template('courses/new.html',
                            categories=categories,
                            users=users,
                            course=course)

    flash(f'Курс {course.name} был успешно добавлен!', 'success')

    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>', methods=['GET','POST'])
def show(course_id):
    course = db.get_or_404(Course, course_id)
    check = db.session.execute(db.select(Review).filter_by(user_id=current_user.get_id())).scalar() # проверка к БД, что пользователь не оставлял review к курсу
    if request.method == "POST" and check is None:
        grade = int(request.form.get("grade", 0))
        comment = request.form.get("comment", 0)
        course.rating_sum += grade
        course.rating_num += 1
        new_reviews = Review(
            rating = grade,
            text = comment,
            course_id = course_id,
            user_id = current_user.id
        )
        db.session.add(new_reviews)
        db.session.commit()
    if request.method == "POST" and check is not None:
        flash(f'Вы уже оставляли отзыв !!!!!!!!!!!', 'danger')
    #5 последний отзывов о курсе
    reviews = db.session.execute(db.select(Review).filter_by(course_id=course_id).order_by(desc(Review.created_at)).limit(5)).scalars()
    review_cur_user = db.session.query(Review).filter(Review.user_id == current_user.id, Review.course_id == course.id).all()
    review_exist = len(review_cur_user) != 0
    return render_template('courses/show.html',course=course, reviews=reviews, review_exist=review_exist, review_cur_user=review_cur_user)

@bp.route('/<int:course_id>/reviews', methods=['GET','POST'])
def show_reviews(course_id):
    course = db.get_or_404(Course, course_id)
    check = None
    check = db.session.execute(db.select(Review).filter_by(user_id=current_user.get_id())).scalar() # проверка к БД, что пользователь не оставлял review к курсу
    if request.method == "POST" and check is None:
        grade = int(request.form.get("grade", 0))
        comment = request.form.get("comment", 0)
        course.rating_sum += grade
        course.rating_num += 1
        new_reviews = Review(
            rating = grade,
            text = comment,
            course_id = course_id,
            user_id = current_user.id
        )
        db.session.add(new_reviews)
        db.session.commit()
    if request.method == "POST" and check is not None:
        flash(f'Вы уже оставляли отзыв !!!!!!!!!!!', 'danger')
    per_page = current_app.config["PER_PAGE"]
    active_page = max(int(request.args.get('page', 1)), 1)
    count_notes = db.session.query(func.count(Review.id)).filter(Review.course_id == course_id).scalar()
    start_page = max(active_page - 1, 1)
    end_page = min(active_page + 1, ceil(count_notes / per_page))
    review_cur_user = db.session.query(Review).filter(Review.user_id == current_user.id, Review.course_id == course.id).all()
    review_exist = len(review_cur_user) != 0
    category = request.args.get('category_of_sorting', None)
    if category is None:
        category = session.get("category", None)
    if category == "positive" :
        reviews = db.session.execute(db.select(Review).filter_by(course_id=course_id).order_by(desc(Review.rating)).limit(per_page).offset((active_page-1)*per_page)).scalars()
        session["category"] = "positive"
    elif category == "negative" :
        reviews = db.session.execute(db.select(Review).filter_by(course_id=course_id).order_by(Review.rating).limit(per_page).offset((active_page-1)*per_page)).scalars()
        session["category"] = "negative"
    else: 
        reviews = db.session.execute(db.select(Review).filter_by(course_id=course_id).order_by(desc(Review.created_at)).limit(per_page).offset((active_page-1)*per_page)).scalars()
        session["category"] = "new_date"
    return render_template('courses/reviews.html',course_id=course_id,review_exist=review_exist,reviews=reviews, per_page=per_page,count_notes=count_notes ,start_page=start_page, end_page=end_page, active_page=active_page, review_cur_user=review_cur_user)



