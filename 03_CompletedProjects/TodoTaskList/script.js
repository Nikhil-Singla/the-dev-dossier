// script.js

// Data structure: { categories: [ {id, name, tasks: [ {id, text, done, daily, lastCompleted } ], xp, level } ] }
let data = { categories: [] };
let currentCategoryId = null;

// Load data from localStorage
function loadData() {
    const saved = localStorage.getItem('taskrpg');
    if (saved) data = JSON.parse(saved);
}
function saveData() {
    localStorage.setItem('taskrpg', JSON.stringify(data));
}

// Generate a simple unique ID (using timestamp)
function generateId() {
    return Date.now().toString();
}

// Render the category list on the left
function renderCategories() {
    const categoryList = document.getElementById('categoryList');
    categoryList.innerHTML = '';
    data.categories.forEach(cat => {
        const li = document.createElement('li');
        li.textContent = cat.name;
        li.dataset.id = cat.id;
        if (cat.id === currentCategoryId) li.classList.add('active');
        li.addEventListener('click', () => selectCategory(cat.id));
        categoryList.appendChild(li);
    });
}

// Select a category to view/edit its tasks
function selectCategory(id) {
    currentCategoryId = id;
    renderCategories();
    renderTasks();
    renderProgress();
}

// Add a new category
function addCategory() {
    const input = document.getElementById('newCategoryInput');
    const name = input.value.trim();
    if (!name) return;
    const cat = {
        id: generateId(),
        name: name,
        tasks: [],
        xp: 0,
        level: 1
    };
    data.categories.push(cat);
    saveData();
    input.value = '';
    renderCategories();
}

// Render the task list for the current category
function renderTasks() {
    const title = document.getElementById('categoryTitle');
    const taskList = document.getElementById('taskList');
    if (!currentCategoryId) {
        title.textContent = 'Select or add a category';
        taskList.innerHTML = '';
        return;
    }
    const cat = data.categories.find(c => c.id === currentCategoryId);
    title.textContent = cat.name;
    taskList.innerHTML = '';
    cat.tasks.forEach(task => {
        const li = document.createElement('li');
        li.textContent = task.text;
        li.dataset.id = task.id;
        if (task.done) li.classList.add('completed');
        // Indicate daily tasks
        if (task.daily) {
            const span = document.createElement('span');
            span.textContent = ' (Daily)';
            span.style.color = 'green';
            li.appendChild(span);
        }
        li.addEventListener('click', () => toggleTask(task.id));
        taskList.appendChild(li);
    });
}

// Add a new task to the current category
function addTask() {
    const input = document.getElementById('newTaskInput');
    const dailyCheckbox = document.getElementById('newTaskDaily');
    const text = input.value.trim();
    if (!text || !currentCategoryId) return;
    const cat = data.categories.find(c => c.id === currentCategoryId);
    const task = {
        id: generateId(),
        text: text,
        done: false,
        daily: dailyCheckbox.checked,
        lastCompleted: null
    };
    cat.tasks.push(task);
    saveData();
    input.value = '';
    dailyCheckbox.checked = false;
    renderTasks();
}

// Toggle task done/undone; award XP if marking done
function toggleTask(taskId) {
    const cat = data.categories.find(c => c.id === currentCategoryId);
    const task = cat.tasks.find(t => t.id === taskId);
    if (!task) return;
    if (!task.done) {
        // Mark task done
        task.done = true;
        task.lastCompleted = new Date().toDateString();
        cat.xp++;
        // Check for level up (every 5 XP)
        const xpForNext = cat.level * 5;
        if (cat.xp >= xpForNext) {
            cat.level++;
            alert(`Category "${cat.name}" reached level ${cat.level}!`);
            unlockSkins(cat.level);
        }
    } else {
        // Uncheck task (done -> undone); no XP deduction
        task.done = false;
    }
    saveData();
    renderTasks();
    renderProgress();
}

// Update the progress display (level and XP)
function renderProgress() {
    if (!currentCategoryId) return;
    const cat = data.categories.find(c => c.id === currentCategoryId);
    document.getElementById('levelDisplay').textContent = cat.level;
    document.getElementById('xpDisplay').textContent = cat.xp;
    document.getElementById('nextLevelXP').textContent = cat.level * 5;
}

// Unlock skins when reaching certain levels
function unlockSkins(level) {
    const skinSelector = document.getElementById('skinSelector');
    if (!skinSelector) return;
    // Example: unlock 'Dark' theme at level 2
    if (level >= 2) {
        const option = document.querySelector('#skinSelector option[value="dark"]');
        if (option) option.disabled = false;
    }
}

// Apply the selected skin/theme
function changeSkin() {
    const skin = document.getElementById('skinSelector').value;
    document.body.className = skin ? 'skin-' + skin : '';
}

// Reset daily tasks on a new day
function dailyResetCheck() {
    const today = new Date().toDateString();
    let changed = false;
    data.categories.forEach(cat => {
        cat.tasks.forEach(task => {
            if (task.daily && task.done && task.lastCompleted !== today) {
                task.done = false;
                changed = true;
            }
        });
    });
    if (changed) {
        saveData();
        renderTasks();
    }
}

// Initialization: load data and set up event handlers
function init() {
    loadData();
    document.getElementById('skinSelector').addEventListener('change', changeSkin);
    document.getElementById('addCategoryBtn').addEventListener('click', addCategory);
    document.getElementById('addTaskBtn').addEventListener('click', addTask);
    renderCategories();
    renderTasks();
    renderProgress();
    dailyResetCheck();
}

document.addEventListener('DOMContentLoaded', init);
