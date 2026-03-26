// Renders a single task object into an <article> DOM element
function renderTask(task) {
  const article = document.createElement('article');
  article.dataset.id = task.id;
  article.className = 'task-card' + (task.completed ? ' completed' : '');

  // Top row: title, reminder, controls
  const topRow = document.createElement('div');
  topRow.className = 'task-top-row';

  const title = document.createElement('span');
  title.className = 'task-title';
  title.textContent = task.title;
  topRow.appendChild(title);

  if (task.remind_at) {
    const remind = document.createElement('span');
    remind.className = 'task-remind';
    remind.textContent = '⏰ ' + new Date(task.remind_at).toLocaleString();
    topRow.appendChild(remind);
  }

  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.className = 'task-complete-toggle';
  checkbox.checked = task.completed;
  checkbox.setAttribute('aria-label', 'Mark complete');
  checkbox.addEventListener('change', () => onToggleComplete(task.id, article));
  topRow.appendChild(checkbox);

  const editBtn = document.createElement('button');
  editBtn.className = 'edit-btn';
  editBtn.textContent = 'Edit';
  editBtn.addEventListener('click', () => onEdit(task, article));
  topRow.appendChild(editBtn);

  const deleteBtn = document.createElement('button');
  deleteBtn.className = 'delete-btn';
  deleteBtn.textContent = 'Delete';
  deleteBtn.addEventListener('click', () => onDelete(task.id, article));
  topRow.appendChild(deleteBtn);

  article.appendChild(topRow);

  // Description row (below)
  if (task.description) {
    const desc = document.createElement('p');
    desc.className = 'task-desc';
    desc.textContent = task.description;
    article.appendChild(desc);
  }

  return article;
}

// Fetches all tasks from the API and populates #task-list
async function loadTasks() {
  const list = document.getElementById('task-list');
  try {
    const res = await fetch('/tasks');
    if (!res.ok) throw new Error(`Failed to load tasks: ${res.status}`);
    const tasks = await res.json();
    list.innerHTML = '';
    tasks.forEach(task => list.appendChild(renderTask(task)));
  } catch (err) {
    console.error(err);
  }
}

// Opens an edit form for title, description, and reminder
function onEdit(task, articleEl) {
  const form = document.createElement('form');
  form.className = 'edit-form';

  const titleInput = document.createElement('input');
  titleInput.type = 'text';
  titleInput.name = 'title';
  titleInput.value = task.title;
  titleInput.required = true;
  titleInput.placeholder = 'Task title';

  const titleLabel = document.createElement('label');
  titleLabel.textContent = 'Title';
  titleLabel.appendChild(titleInput);
  form.appendChild(titleLabel);

  const descTextarea = document.createElement('textarea');
  descTextarea.name = 'description';
  descTextarea.value = task.description || '';
  descTextarea.placeholder = 'Optional description';

  const descLabel = document.createElement('label');
  descLabel.textContent = 'Description';
  descLabel.appendChild(descTextarea);
  form.appendChild(descLabel);

  const reminderInput = document.createElement('input');
  reminderInput.type = 'datetime-local';
  reminderInput.name = 'remind_at';
  if (task.remind_at) {
    // Convert ISO string to datetime-local format (YYYY-MM-DDTHH:MM)
    reminderInput.value = task.remind_at.slice(0, 16);
  }

  const reminderLabel = document.createElement('label');
  reminderLabel.textContent = 'Reminder';
  reminderLabel.appendChild(reminderInput);
  form.appendChild(reminderLabel);

  const saveBtn = document.createElement('button');
  saveBtn.type = 'submit';
  saveBtn.textContent = 'Save';
  form.appendChild(saveBtn);

  const cancelBtn = document.createElement('button');
  cancelBtn.type = 'button';
  cancelBtn.textContent = 'Cancel';
  cancelBtn.addEventListener('click', () => articleEl.replaceWith(renderTask(task)));
  form.appendChild(cancelBtn);

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const res = await fetch(`/tasks/${task.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: titleInput.value, description: descTextarea.value }),
    });
    if (!res.ok) return;
    let updatedTask = await res.json();

    if (reminderInput.value) {
      const remRes = await fetch(`/tasks/${task.id}/reminder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ remind_at: new Date(reminderInput.value).toISOString() }),
      });
      if (remRes.ok) {
        updatedTask = await remRes.json();
      }
    }

    articleEl.replaceWith(renderTask(updatedTask));
  });

  articleEl.innerHTML = '';
  articleEl.appendChild(form);
}

async function onDelete(taskId, articleEl) {
  const res = await fetch(`/tasks/${taskId}`, { method: 'DELETE' });
  if (res.ok) {
    articleEl.remove();
  }
}

async function onToggleComplete(taskId, articleEl) {
  const res = await fetch(`/tasks/${taskId}/complete`, { method: 'POST' });
  if (res.ok) {
    const updatedTask = await res.json();
    articleEl.classList.toggle('completed', updatedTask.completed);
    const checkbox = articleEl.querySelector('.task-complete-toggle');
    if (checkbox) checkbox.checked = updatedTask.completed;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadTasks();

  const taskForm = document.getElementById('task-form');
  if (taskForm) {
    taskForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('title').value;
      const description = document.getElementById('description').value;

      const res = await fetch('/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description }),
      });

      if (res.status === 201) {
        const newTask = await res.json();
        document.getElementById('task-list').appendChild(renderTask(newTask));
        taskForm.reset();
      }
    });
  }
});
