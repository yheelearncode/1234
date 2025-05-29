from flask import Blueprint, render_template, request, jsonify
from app.models.alarm import Alarm, Memo
from app import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

# 알람 관련 API
@main_bp.route('/api/alarms', methods=['GET'])
def get_alarms():
    alarms = Alarm.query.all()
    return jsonify([alarm.to_dict() for alarm in alarms])

@main_bp.route('/api/alarms', methods=['POST'])
def create_alarm():
    data = request.json
    alarm = Alarm(
        time=data['time'],
        label=data.get('label'),
        days=data.get('days'),
        specific_date=datetime.strptime(data['specific_date'], '%Y-%m-%d').date() if data.get('specific_date') else None
    )
    db.session.add(alarm)
    db.session.commit()
    return jsonify(alarm.to_dict()), 201

@main_bp.route('/api/alarms/<int:alarm_id>', methods=['PUT'])
def update_alarm(alarm_id):
    alarm = Alarm.query.get_or_404(alarm_id)
    data = request.json
    
    alarm.time = data.get('time', alarm.time)
    alarm.label = data.get('label', alarm.label)
    alarm.days = data.get('days', alarm.days)
    alarm.specific_date = datetime.strptime(data['specific_date'], '%Y-%m-%d').date() if data.get('specific_date') else alarm.specific_date
    alarm.is_active = data.get('is_active', alarm.is_active)
    
    db.session.commit()
    return jsonify(alarm.to_dict())

@main_bp.route('/api/alarms/<int:alarm_id>', methods=['DELETE'])
def delete_alarm(alarm_id):
    alarm = Alarm.query.get_or_404(alarm_id)
    db.session.delete(alarm)
    db.session.commit()
    return '', 204

# 메모 관련 API
@main_bp.route('/api/memos', methods=['GET'])
def get_memos():
    memos = Memo.query.all()
    return jsonify([memo.to_dict() for memo in memos])

@main_bp.route('/api/memos', methods=['POST'])
def create_memo():
    data = request.json
    memo = Memo(
        content=data['content'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else None
    )
    db.session.add(memo)
    db.session.commit()
    return jsonify(memo.to_dict()), 201

@main_bp.route('/api/memos/<int:memo_id>', methods=['PUT'])
def update_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    data = request.json
    
    memo.content = data.get('content', memo.content)
    memo.date = datetime.strptime(data['date'], '%Y-%m-%d').date() if data.get('date') else memo.date
    
    db.session.commit()
    return jsonify(memo.to_dict())

@main_bp.route('/api/memos/<int:memo_id>', methods=['DELETE'])
def delete_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    db.session.delete(memo)
    db.session.commit()
    return '', 204 