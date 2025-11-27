const API_URL = 'http://localhost:3000/api';
const USER_ID = 1; // Hardcoded for single user demo

class App {
    constructor() {
        this.content = document.getElementById('app-content');
        this.currentView = 'chat';
        this.init();
    }

    init() {
        this.navigate('chat');
        this.setupMobileMenu();
    }

    navigate(view) {
        this.currentView = view;
        this.updateNav();

        if (view === 'chat') this.renderChat();
        else if (view === 'analytics') this.renderAnalytics();
        else if (view === 'system') this.renderSystem();
    }

    updateNav() {
        document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active-nav'));
        const active = document.getElementById(`nav-${this.currentView}`);
        if (active) active.classList.add('active-nav');
    }

    setupMobileMenu() {
        // Simple toggle for mobile (omitted for brevity, can add if needed)
    }

    // --- CHAT VIEW ---
    async renderChat() {
        this.content.innerHTML = `
            <div class="flex flex-col h-full">
                <div id="chat-history" class="flex-1 overflow-y-auto p-6 space-y-4">
                    <!-- Messages go here -->
                </div>
                <div class="p-4 bg-surface/50 border-t border-white/10">
                    <!-- Agent Actions -->
                    <div class="flex gap-2 mb-3 overflow-x-auto pb-2">
                        <button onclick="app.triggerAgent('planner')" class="whitespace-nowrap px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full text-sm text-gray-300 transition-all flex items-center gap-2">
                            <i class="fa-solid fa-calendar-day text-primary"></i> Daily Plan
                        </button>
                        <button onclick="app.triggerAgent('resource')" class="whitespace-nowrap px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full text-sm text-gray-300 transition-all flex items-center gap-2">
                            <i class="fa-solid fa-spa text-green-400"></i> Coping Strategy
                        </button>
                    </div>

                    <form id="chat-form" class="flex gap-3 max-w-4xl mx-auto">
                        <input type="text" id="chat-input" placeholder="How are you feeling today?" 
                            class="flex-1 bg-dark/50 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-primary text-white placeholder-gray-500 transition-all">
                        <button type="submit" class="bg-gradient-to-r from-primary to-secondary text-white px-6 py-3 rounded-xl font-medium hover:opacity-90 transition-all shadow-lg shadow-primary/20">
                            <i class="fa-solid fa-paper-plane"></i>
                        </button>
                    </form>
                </div>
            </div>
        `;

        this.loadChatHistory();

        document.getElementById('chat-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
    }

    async loadChatHistory() {
        try {
            const res = await fetch(`${API_URL}/history?user_id=${USER_ID}`);
            const history = await res.json();
            const container = document.getElementById('chat-history');
            container.innerHTML = '';
            history.forEach(msg => this.appendMessage(msg.role, msg.content));
            this.scrollToBottom();
        } catch (e) {
            console.error("Failed to load history", e);
        }
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (!message) return;

        input.value = '';
        this.appendMessage('user', message);
        this.scrollToBottom();
        this.showTyping();

        try {
            const res = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: USER_ID, message })
            });
            const data = await res.json();
            this.removeTyping();
            this.appendMessage('model', data.response);
            this.scrollToBottom();
        } catch (e) {
            this.removeTyping();
            this.appendMessage('model', "I'm having trouble connecting right now. Please try again.");
        }
    }

    async triggerAgent(type) {
        this.showTyping();
        try {
            const endpoint = type === 'planner' ? '/agent/planner' : '/agent/resource';
            // For resource agent, we could pass current mood if we tracked it, but for now generic or last message context
            const body = type === 'resource' ? { mood: 'stress' } : {};

            const res = await fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            const data = await res.json();
            this.removeTyping();
            this.appendMessage('model', data.response);
            this.scrollToBottom();
        } catch (e) {
            this.removeTyping();
            this.appendMessage('model', "Agent unavailable.");
        }
    }

    appendMessage(role, text) {
        const container = document.getElementById('chat-history');
        const isUser = role === 'user';

        const html = `
            <div class="flex ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in">
                <div class="message-bubble p-4 rounded-2xl ${isUser ? 'bg-primary text-white rounded-tr-none' : 'bg-surface text-gray-200 rounded-tl-none border border-white/5'}">
                    <p class="leading-relaxed">${text}</p>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
    }

    showTyping() {
        const container = document.getElementById('chat-history');
        const html = `
            <div id="typing-indicator" class="flex justify-start animate-fade-in">
                <div class="bg-surface p-4 rounded-2xl rounded-tl-none border border-white/5">
                    <div class="typing-indicator">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
        this.scrollToBottom();
    }

    removeTyping() {
        const el = document.getElementById('typing-indicator');
        if (el) el.remove();
    }

    scrollToBottom() {
        const container = document.getElementById('chat-history');
        container.scrollTop = container.scrollHeight;
    }

    // --- ANALYTICS VIEW ---
    async renderAnalytics() {
        this.content.innerHTML = `
            <div class="p-8 h-full overflow-y-auto">
                <h2 class="text-3xl font-bold mb-6">Mood Analytics</h2>
                
                <!-- Stats Row -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <div class="glass-panel p-6 rounded-2xl flex items-center gap-4">
                        <div class="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center text-primary text-xl">
                            <i class="fa-solid fa-comments"></i>
                        </div>
                        <div>
                            <div class="text-gray-400 text-sm">Total Interactions</div>
                            <div class="text-2xl font-bold" id="stat-total-chats">...</div>
                        </div>
                    </div>
                    <div class="glass-panel p-6 rounded-2xl flex items-center gap-4">
                        <div class="w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center text-green-400 text-xl">
                            <i class="fa-solid fa-smile"></i>
                        </div>
                        <div>
                            <div class="text-gray-400 text-sm">Average Mood</div>
                            <div class="text-2xl font-bold" id="stat-avg-mood">...</div>
                        </div>
                    </div>
                    <div class="glass-panel p-6 rounded-2xl flex items-center gap-4">
                        <div class="w-12 h-12 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 text-xl">
                            <i class="fa-solid fa-calendar-check"></i>
                        </div>
                        <div>
                            <div class="text-gray-400 text-sm">Status</div>
                            <div class="text-2xl font-bold">Active</div>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Line Chart -->
                    <div class="glass-panel p-6 rounded-2xl">
                        <h3 class="text-xl font-semibold mb-4 text-gray-300">Sentiment Trend</h3>
                        <canvas id="sentimentChart"></canvas>
                    </div>
                    
                    <!-- Pie Chart & Insights -->
                    <div class="space-y-6">
                        <div class="glass-panel p-6 rounded-2xl">
                            <h3 class="text-xl font-semibold mb-4 text-gray-300">Mood Distribution</h3>
                            <div class="h-64 flex justify-center">
                                <canvas id="distributionChart"></canvas>
                            </div>
                        </div>
                        <div class="glass-panel p-6 rounded-2xl">
                            <h3 class="text-xl font-semibold mb-4 text-gray-300">AI Insight</h3>
                            <p class="text-gray-400" id="analytics-insight">Gathering data...</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        this.loadAnalyticsData();
    }

    async loadAnalyticsData() {
        try {
            const res = await fetch(`${API_URL}/analytics?user_id=${USER_ID}`);
            const data = await res.json();
            console.log("Analytics Data:", data);

            if (!data || data.length === 0) {
                document.getElementById('stat-total-chats').textContent = '0';
                document.getElementById('stat-avg-mood').textContent = 'N/A';
                document.getElementById('analytics-insight').textContent = "No data available yet. Start chatting!";
                return;
            }

            // Helper to parse SQLite date
            const parseDate = (dateStr) => {
                return new Date(dateStr.replace(' ', 'T'));
            };

            // 1. Line Chart
            const ctx = document.getElementById('sentimentChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.map(d => parseDate(d.timestamp).toLocaleDateString()),
                    datasets: [{
                        label: 'Mood Score',
                        data: data.map(d => d.score),
                        borderColor: '#818cf8',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#6366f1'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { beginAtZero: false, grid: { color: 'rgba(255,255,255,0.05)' } },
                        x: { grid: { display: false } }
                    }
                }
            });

            // 2. Stats Calculation
            const totalChats = data.length;
            const avgScore = totalChats > 0 ? data.reduce((acc, curr) => acc + curr.score, 0) / totalChats : 0;

            document.getElementById('stat-total-chats').textContent = totalChats;
            document.getElementById('stat-avg-mood').textContent = avgScore.toFixed(2);

            // 3. Distribution Chart (Pie)
            const positive = data.filter(d => d.score > 0.3).length;
            const negative = data.filter(d => d.score < -0.3).length;
            const neutral = totalChats - positive - negative;

            const ctxPie = document.getElementById('distributionChart').getContext('2d');
            new Chart(ctxPie, {
                type: 'doughnut',
                data: {
                    labels: ['Positive', 'Neutral', 'Negative'],
                    datasets: [{
                        data: [positive, neutral, negative],
                        backgroundColor: ['#4ade80', '#94a3b8', '#f87171'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom', labels: { color: '#cbd5e1' } }
                    }
                }
            });

            // 4. Insights Text
            let insightText = "Start chatting to get insights!";
            let insightColor = "text-gray-400";

            if (totalChats > 0) {
                if (avgScore > 0.3) {
                    insightText = "Your mood has been generally positive. Keep up the good work!";
                    insightColor = "text-green-400";
                } else if (avgScore < -0.3) {
                    insightText = "It seems you've been having a tough time. Remember to use the Coping Strategies.";
                    insightColor = "text-red-400";
                } else {
                    insightText = "Your mood has been balanced. Consistency is key!";
                    insightColor = "text-blue-400";
                }
            }

            const insightContainer = document.getElementById('analytics-insight');
            if (insightContainer) {
                insightContainer.textContent = insightText;
                insightContainer.className = insightColor;
            }

        } catch (e) {
            console.error("Failed to load analytics", e);
            document.getElementById('analytics-insight').textContent = "Failed to load analytics data.";
        }
    }

    async renderSystem() {
        this.content.innerHTML = `
            <div class="p-8 h-full overflow-y-auto">
                <h2 class="text-3xl font-bold mb-6">System Health</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="system-stats">
                    <div class="glass-panel p-6 rounded-2xl animate-pulse">Loading...</div>
                </div>
                
                <div class="mt-8">
                    <h3 class="text-xl font-bold mb-4">Data Management</h3>
                    <button onclick="app.downloadData()" class="bg-surface border border-white/10 hover:bg-white/5 text-white px-6 py-3 rounded-xl transition-all flex items-center gap-2">
                        <i class="fa-solid fa-download"></i> Download My Data
                    </button>
                </div>
            </div>
        `;

        this.loadSystemStatus();
    }

    async downloadData() {
        try {
            const res = await fetch(`${API_URL}/export?user_id=${USER_ID}`);
            const data = await res.json();

            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `moodnestai_data_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (e) {
            console.error("Failed to download data", e);
            alert("Failed to download data. Please try again.");
        }
    }

    async loadSystemStatus() {
        try {
            const res = await fetch(`${API_URL}/system`);
            const status = await res.json();

            const container = document.getElementById('system-stats');
            container.innerHTML = `
                <div class="glass-panel p-6 rounded-2xl">
                    <div class="text-gray-400 text-sm mb-1">Status</div>
                    <div class="text-2xl font-bold text-green-400 capitalize">${status.status}</div>
                </div>
                <div class="glass-panel p-6 rounded-2xl">
                    <div class="text-gray-400 text-sm mb-1">Platform</div>
                    <div class="text-2xl font-bold">${status.platform}</div>
                </div>
                <div class="glass-panel p-6 rounded-2xl">
                    <div class="text-gray-400 text-sm mb-1">CPU Usage</div>
                    <div class="text-2xl font-bold">${status.cpu_percent}%</div>
                </div>
                <div class="glass-panel p-6 rounded-2xl">
                    <div class="text-gray-400 text-sm mb-1">Memory Usage</div>
                    <div class="text-2xl font-bold">${status.memory_percent}%</div>
                </div>
            `;
        } catch (e) {
            console.error("Failed to load system status", e);
        }
    }
}
const app = new App();
