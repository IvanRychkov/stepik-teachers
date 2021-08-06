from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Промежуточная таблица учителей и целей
teachers_goals = db.Table(
    'teachers_goals',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('goal_name', db.String(), db.ForeignKey('goals.name'))
)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    about = db.Column(db.String())
    rating = db.Column(db.Float)
    picture = db.Column(db.String())
    price = db.Column(db.Integer)
    free = db.Column(db.JSON())
    bookings = db.relationship('Booking')
    goals = db.relationship('Goal', secondary=teachers_goals, back_populates='teachers')


class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    ru_name = db.Column(db.String(), unique=True)
    emoji = db.Column(db.String())
    teachers = db.relationship('Teacher', secondary=teachers_goals, back_populates='goals')


class Weekday(db.Model):
    __tablename__ = 'weekdays'
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.VARCHAR(3), unique=True)
    ru_name = db.Column(db.String())


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    phone = db.Column(db.String())
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    teacher = db.relationship('Teacher', back_populates='bookings')
    day_short_name = db.Column(db.VARCHAR(3), db.ForeignKey('weekdays.short_name'))
    weekday = db.relationship('Weekday')
    time = db.Column(db.Time)


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
    time = db.Column(db.String())
    goal = db.relationship('Goal', uselist=False)

