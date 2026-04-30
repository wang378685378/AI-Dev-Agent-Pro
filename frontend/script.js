const statusMap = {
    'start': { icon: '🧠', text: '分析需求', emoji: '🧠' },
    'generate': { icon: '📦', text: '生成代码', emoji: '📦' },
    'test': { icon: '🧪', text: '测试', emoji: '🧪' },
    'fix': { icon: '🔧', text: '修复', emoji: '🔧' },
    'done': { icon: '✅', text: '完成', emoji: '✅' },
    'error': { icon: '❌', text: '错误', emoji: '❌' }
};

document.getElementById('generate-btn').addEventListener('click', () => {
    const requirement = document.getElementById('requirement').value.trim();
    if (!requirement) {
        alert('请输入需求');
        return;
    }

    const btn = document.getElementById('generate-btn');
    const logDiv = document.getElementById('log');
    const outputDiv = document.getElementById('output');
    
    btn.disabled = true;
    btn.textContent = '⏳ 生成中...';
    logDiv.textContent = '';
    outputDiv.textContent = '';
    
    Object.keys(statusMap).forEach(status => {
        const step = document.getElementById(`step-${status}`);
        if (step) {
            step.className = 'step';
            step.querySelector('.icon').textContent = '⏳';
        }
    });

    const url = `http://localhost:8000/generate?requirement=${encodeURIComponent(requirement)}`;
    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const statusInfo = statusMap[data.status];
            
            if (statusInfo) {
                logDiv.textContent += `${statusInfo.emoji} [${data.status}] ${data.message}\n`;
                
                Object.keys(statusMap).forEach(s => {
                    const step = document.getElementById(`step-${s}`);
                    if (!step) return;
                    const statusIndex = Object.keys(statusMap).indexOf(s);
                    const currentIndex = Object.keys(statusMap).indexOf(data.status);
                    if (s === data.status) {
                        step.className = 'step active';
                        step.querySelector('.icon').textContent = statusInfo.icon;
                    } else if (statusIndex < currentIndex) {
                        step.className = 'step completed';
                        step.querySelector('.icon').textContent = statusMap[s].icon;
                    }
                });
            }

            if (data.files) {
                outputDiv.textContent = JSON.stringify(data.files, null, 2);
            }

            if (data.status === 'done' || data.status === 'error') {
                eventSource.close();
                btn.disabled = false;
                btn.textContent = '🚀 开始生成';
            }
        } catch (e) {
            console.error('Parse error:', e);
        }
    };

    eventSource.onerror = () => {
        eventSource.close();
        btn.disabled = false;
        btn.textContent = '🚀 开始生成';
        logDiv.textContent += '❌ 连接错误\n';
    };
});
