// script.js

// Data structure: { categories: [ {id, name, tasks: [ {id, text, done, daily, lastCompleted } ], xp, level } ] }
let data = { categories: [] };
let currentCategoryId = null;

/* -----------------------
   PERSISTENCE: loadData()
   - Purpose: read saved app state from localStorage and populate `data`.
   - Inputs: none (reads "taskrpg" key from localStorage).
   - Outputs: sets the module-scoped `data` variable if saved data exists.
   - Side-effects: none beyond reading/parsing localStorage.
   - Notes: silently ignores parse errors (assumes valid JSON).
   ----------------------- */
function loadData() {
    const saved = localStorage.getItem('taskrpg');
    if (saved) data = JSON.parse(saved);
}

/* -----------------------
   PERSISTENCE: saveData()
   - Purpose: serialize current `data` and persist to localStorage.
   - Inputs: uses the module-scoped `data`.
   - Outputs: writes to localStorage key "taskrpg".
   - Side-effects: overwrites previous "taskrpg" value in localStorage.
   ----------------------- */
function saveData() {
    localStorage.setItem('taskrpg', JSON.stringify(data));
}

/* -----------------------
   ID GENERATION: generateId()
   - Purpose: create a simple (non-cryptographic) unique identifier for categories/tasks.
   - Inputs: none.
   - Outputs: returns a string based on the current timestamp.
   - Side-effects: none.
   - Notes: collisions are extremely unlikely in normal UI usage but possible if called multiple times in the same ms.
   ----------------------- */
function generateId() {
    return Date.now().toString();
}

/* -----------------------
   RENDER: renderCategories()
   - Purpose: draw the category list in the left-hand UI.
   - Inputs: reads `data.categories` and `currentCategoryId`.
   - Outputs: updates the DOM element with id "categoryList".
   - Side-effects: attaches click handlers to each created list item that call selectCategory().
   ----------------------- */
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

/* -----------------------
   NAVIGATION: selectCategory(id)
   - Purpose: set the active category for the UI and update visible details.
   - Inputs: id (string) - the category id to select.
   - Outputs: updates module-scoped `currentCategoryId`.
   - Side-effects: re-renders categories, tasks, and progress displays.
   ----------------------- */
function selectCategory(id) {
    currentCategoryId = id;
    renderCategories();
    renderTasks();
    renderProgress();
}

/* -----------------------
   MUTATION: addCategory()
   - Purpose: create a new category from the UI input and persist it.
   - Inputs: reads the #newCategoryInput element value.
   - Outputs: appends a new category object to `data.categories`.
   - Side-effects: saves to localStorage, clears the input, and re-renders category list.
   - Validation: ignores empty/whitespace-only names.
   ----------------------- */
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

/* -----------------------
   RENDER: renderTasks()
   - Purpose: show tasks for the currently selected category in the main pane.
   - Inputs: reads `currentCategoryId` and `data.categories`.
   - Outputs: updates #categoryTitle and #taskList in the DOM.
   - Side-effects: attaches click handlers to task items that toggle completion via toggleTask().
   - Edge-cases: if no category selected, clears task list and prompts user.
   ----------------------- */
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

/* -----------------------
   MUTATION: addTask()
   - Purpose: add a new task under the currently selected category.
   - Inputs: reads #newTaskInput and #newTaskDaily checkbox; requires currentCategoryId to be set.
   - Outputs: pushes a new task object into the category's tasks array.
   - Side-effects: saves data to localStorage, clears inputs, re-renders tasks.
   - Validation: ignores empty task text or when no category is selected.
   ----------------------- */
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

/* -----------------------
   MUTATION: toggleTask(taskId)
   - Purpose: toggle a task between done/undone; award XP when marking done.
   - Inputs: taskId (string) identifying the task within the current category.
   - Outputs: updates task.done, task.lastCompleted, category xp/level as needed.
   - Side-effects: persists changes, re-renders tasks and progress; may show alert on level up.
   - Rules: marking done increments xp by 1; level up occurs when xp >= level * 5.
   ----------------------- */
function toggleTask(taskId) {
    const cat = data.categories.find(c => c.id === currentCategoryId);
    const task = cat.tasks.find(t => t.id === taskId);
    if (!task) return;
    if (!task.done) {
        // Mark task done
        task.done = true;
        task.lastCompleted = new Date().toDateString();
        cat.xp++;
        // Check for level up (every 5 XP per level)
        const xpForNext = cat.level * 5;
        if (cat.xp >= xpForNext) {
            cat.level++;
            alert(`Category "${cat.name}" reached level ${cat.level}!`);
            unlockSkins(cat.level);
        }
    } else {
        // Uncheck task (done -> undone); no XP deduction by design
        task.done = false;
    }
    saveData();
    renderTasks();
    renderProgress();
}

/* -----------------------
   RENDER: renderProgress()
   - Purpose: update the level and XP indicators in the UI for the current category, using a horizontal XP bar.
   - Inputs: uses `currentCategoryId` to find the category object and read level/xp.
   - Outputs: writes to #levelDisplay, #xpDisplay, #nextLevelXP, and sets #xpBar width.
   - Side-effects: updates aria-valuenow on the progress container for accessibility.
   - Edge-cases: does nothing when no category is selected.
   ----------------------- */
function renderProgress() {
    if (!currentCategoryId) return;
    const cat = data.categories.find(c => c.id === currentCategoryId);
    document.getElementById('levelDisplay').textContent = cat.level;
    document.getElementById('xpDisplay').textContent = cat.xp;
    const xpForNext = cat.level * 5;
    document.getElementById('nextLevelXP').textContent = xpForNext;

    // Compute percentage fill for the XP bar (cap at 100)
    const percent = Math.min(100, Math.round((cat.xp / xpForNext) * 100));
    const xpBar = document.getElementById('xpBar');
    if (xpBar) xpBar.style.width = percent + '%';

    // Update progressbar aria value (optional)
    const bar = document.querySelector('.xp-bar');
    if (bar) bar.setAttribute('aria-valuenow', percent.toString());
}

/* -----------------------
   UNLOCKS: unlockSkins(level)
   - Purpose: enable UI skin options based on category level milestones.
   - Inputs: level (number) - the newly reached level.
   - Outputs: manipulates the DOM <option> disabled property for available skins.
   - Side-effects: toggles availability of the "dark" option when level >= 2.
   - Notes: This is UI-only; actual style changes are applied via changeSkin().
   ----------------------- */
function unlockSkins(level) {
    const skinSelector = document.getElementById('skinSelector');
    if (!skinSelector) return;
    // Example: unlock 'Dark' theme at level 2
    if (level >= 2) {
        const option = document.querySelector('#skinSelector option[value="dark"]');
        if (option) option.disabled = false;
    }
}

/* -----------------------
   UI: changeSkin()
   - Purpose: apply the selected skin by toggling a CSS class on <body>.
   - Inputs: reads value of #skinSelector.
   - Outputs: sets document.body.className to "skin-<value>" or clears it.
   - Side-effects: affects page appearance via CSS.
   ----------------------- */
function changeSkin() {
    const skin = document.getElementById('skinSelector').value;
    document.body.className = skin ? 'skin-' + skin : '';
}

/* -----------------------
   DAILY MAINTENANCE: dailyResetCheck()
   - Purpose: reset tasks that are marked "daily" if they were completed on a prior day.
   - Inputs: compares each task.lastCompleted to today's date string.
   - Outputs: sets task.done = false for daily tasks not completed today.
   - Side-effects: persists changes and re-renders tasks if any were reset.
   - Notes: idempotent if called multiple times on the same day.
   ----------------------- */
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

/* -----------------------
   RESET: resetAll()
   - Purpose: clear application data from localStorage/sessionStorage and do a full page reload.
   - Inputs: none.
   - Outputs: removes "taskrpg" key from localStorage and clears sessionStorage.
   - Side-effects: forces a location.reload() which resets in-memory state and the UI.
   - Notes: this is a hard reset for client-side state (does not affect HttpOnly cookies or server state).
   ----------------------- */
function resetAll() {
    // Clear app storage
    localStorage.removeItem('taskrpg'); // remove app data
    // Optionally clear sessionStorage
    sessionStorage.clear();
    // Reload to start fresh
    location.reload();
}

/* -----------------------
   BOOTSTRAP: init()
   - Purpose: initialize the app on DOMContentLoaded: load data, bind UI handlers, and render initial state.
   - Inputs: none (reads DOM elements by id).
   - Outputs: registers event listeners and triggers initial render functions.
   - Side-effects: attaches listeners to skin selector, add buttons, and reset button; runs daily reset check.
   ----------------------- */
function init() {
    loadData();
    document.getElementById('skinSelector').addEventListener('change', changeSkin);
    document.getElementById('addCategoryBtn').addEventListener('click', addCategory);
    document.getElementById('addTaskBtn').addEventListener('click', addTask);

    // Reset button hook
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) resetBtn.addEventListener('click', resetAll);

    renderCategories();
    renderTasks();
    renderProgress();
    dailyResetCheck();
}

document.addEventListener('DOMContentLoaded', init);
