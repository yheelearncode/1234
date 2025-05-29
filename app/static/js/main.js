document.addEventListener('DOMContentLoaded', function() {
    // 초기 데이터 로드
    loadAlarms();
    loadMemos();

    // 폼 제출 이벤트 리스너
    document.getElementById('alarmForm').addEventListener('submit', handleAlarmSubmit);
    document.getElementById('memoForm').addEventListener('submit', handleMemoSubmit);
});

// 알람 관련 함수
async function loadAlarms() {
    try {
        const response = await fetch('/api/alarms');
        const alarms = await response.json();
        displayAlarms(alarms);
    } catch (error) {
        console.error('알람 로드 중 오류 발생:', error);
        alert('알람을 불러오는데 실패했습니다.');
    }
}

function displayAlarms(alarms) {
    const alarmsList = document.getElementById('alarmsList');
    alarmsList.innerHTML = '';

    alarms.forEach(alarm => {
        const item = document.createElement('div');
        item.className = 'list-group-item';
        
        const daysText = alarm.days ? 
            alarm.days.split(',').map(d => '일월화수목금토'[parseInt(d)]).join(', ') : 
            (alarm.specific_date ? `${alarm.specific_date}` : '반복 없음');

        item.innerHTML = `
            <div class="alarm-info">
                <div class="alarm-time">${alarm.time}</div>
                <div class="alarm-label">${alarm.label || '알람'}</div>
                <div class="alarm-days">${daysText}</div>
            </div>
            <div class="alarm-actions">
                <button class="btn btn-sm btn-outline-danger" onclick="deleteAlarm(${alarm.id})">삭제</button>
                <button class="btn btn-sm btn-outline-primary" onclick="toggleAlarm(${alarm.id}, ${!alarm.is_active})">
                    ${alarm.is_active ? '비활성화' : '활성화'}
                </button>
            </div>
        `;
        alarmsList.appendChild(item);
    });
}

async function handleAlarmSubmit(event) {
    event.preventDefault();
    
    const time = document.getElementById('alarmTime').value;
    const label = document.getElementById('alarmLabel').value;
    const specificDate = document.getElementById('specificDate').value;
    
    const days = Array.from(document.querySelectorAll('.btn-check'))
        .map((checkbox, index) => checkbox.checked ? index : null)
        .filter(day => day !== null)
        .join(',');

    try {
        const response = await fetch('/api/alarms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                time,
                label,
                days: days || null,
                specific_date: specificDate || null
            })
        });

        if (response.ok) {
            event.target.reset();
            loadAlarms();
        } else {
            throw new Error('서버 오류');
        }
    } catch (error) {
        console.error('알람 추가 중 오류 발생:', error);
        alert('알람 추가에 실패했습니다.');
    }
}

async function deleteAlarm(id) {
    if (!confirm('이 알람을 삭제하시겠습니까?')) return;

    try {
        const response = await fetch(`/api/alarms/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadAlarms();
        } else {
            throw new Error('서버 오류');
        }
    } catch (error) {
        console.error('알람 삭제 중 오류 발생:', error);
        alert('알람 삭제에 실패했습니다.');
    }
}

async function toggleAlarm(id, isActive) {
    try {
        const response = await fetch(`/api/alarms/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                is_active: isActive
            })
        });

        if (response.ok) {
            loadAlarms();
        } else {
            throw new Error('서버 오류');
        }
    } catch (error) {
        console.error('알람 상태 변경 중 오류 발생:', error);
        alert('알람 상태 변경에 실패했습니다.');
    }
}

// 메모 관련 함수
async function loadMemos() {
    try {
        const response = await fetch('/api/memos');
        const memos = await response.json();
        displayMemos(memos);
    } catch (error) {
        console.error('메모 로드 중 오류 발생:', error);
        alert('메모를 불러오는데 실패했습니다.');
    }
}

function displayMemos(memos) {
    const memosList = document.getElementById('memosList');
    memosList.innerHTML = '';

    memos.forEach(memo => {
        const item = document.createElement('div');
        item.className = 'list-group-item';
        
        item.innerHTML = `
            <div class="memo-info">
                <div class="memo-content">${memo.content}</div>
                ${memo.date ? `<div class="memo-date">${memo.date}</div>` : ''}
            </div>
            <div class="memo-actions">
                <button class="btn btn-sm btn-outline-danger" onclick="deleteMemo(${memo.id})">삭제</button>
            </div>
        `;
        memosList.appendChild(item);
    });
}

async function handleMemoSubmit(event) {
    event.preventDefault();
    
    const content = document.getElementById('memoContent').value;
    const date = document.getElementById('memoDate').value;

    try {
        const response = await fetch('/api/memos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content,
                date: date || null
            })
        });

        if (response.ok) {
            event.target.reset();
            loadMemos();
        } else {
            throw new Error('서버 오류');
        }
    } catch (error) {
        console.error('메모 추가 중 오류 발생:', error);
        alert('메모 추가에 실패했습니다.');
    }
}

async function deleteMemo(id) {
    if (!confirm('이 메모를 삭제하시겠습니까?')) return;

    try {
        const response = await fetch(`/api/memos/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadMemos();
        } else {
            throw new Error('서버 오류');
        }
    } catch (error) {
        console.error('메모 삭제 중 오류 발생:', error);
        alert('메모 삭제에 실패했습니다.');
    }
} 