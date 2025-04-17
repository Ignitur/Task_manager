
document.getElementById("task-form").addEventListener("submit", async function(event) {
	event.preventDefault();
	let taskTitle = document.getElementById("task-title").value;
	let taskDescription = document.getElementById("task-description").value;
	let taskDeadline = document.getElementById("task-deadline").value;

	const response = await fetch("/tasks", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ 
			title: taskTitle, 
			description: taskDescription, 
			deadline: taskDeadline
			})
	});

	if (response.ok) {
		location.reload();
	} else {
		alert("Ошибка при добавлении задачи");
	}
});

async function deleteTask(taskId) {
	let response = await fetch(`/tasks/${taskId}`, { method: "DELETE" });

	if (response.ok) {
		location.reload();
	}
}

let currentTaskId = null;

function editTask(taskId) {
	let taskElement = document.querySelector(`[data-id='${taskId}']`);
	if (!taskElement) return;


	let taskTitleElement = taskElement.querySelector(".task-title");
	let taskDescriptionElement = taskElement.querySelector(".task-description");
	let taskDeadlineElement = taskElement.querySelector(".task-deadline");

	let taskTitle = taskTitleElement ? taskTitleElement.innerText : "";
	let taskDescription = taskDescriptionElement ? taskDescriptionElement.innerText : "";
	let taskDeadline = taskDeadlineElement ? taskDeadlineElement.innerText : "";

	document.getElementById("editTaskTitle").value = taskTitle;
	document.getElementById("editTaskDescription").value = taskDescription;
	document.getElementById("editTaskDeadline").value = taskDeadline;

	document.getElementById("editTaskModal").style.display = "block";
	currentTaskId = taskId;
}

document.getElementById("saveTask").addEventListener("click", async function () {
	if (currentTaskId === null) return;

	let newTitle = document.getElementById("editTaskTitle").value;
	let newDescription = document.getElementById("editTaskDescription").value;
	let newDeadline = document.getElementById("editTaskDeadline").value;

	let response = await fetch(`/tasks/${currentTaskId}`, {
		method: "PUT",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ 
			title: newTitle, 
			description: newDescription,
			deadline: newDeadline
		})
	});

	if (response.ok) {
		location.reload();
	} else {
		alert("ERROR when edit");
	}
});

document.getElementById("closeModal").addEventListener("click", function () {
	document.getElementById("editTaskModal").style.display = "none";
	currentTaskId = null
});


document.querySelectorAll(".task").forEach(task => {
	let deadlineText = task.querySelector(".task-deadline").innerText.trim();
	if (deadlineText.includes("None")) return;

	let deadlineDateStr = new Date(deadlineText.replace("Дедлайн: ", "").trim());
	let deadlineDate = new Date(deadlineDateStr);

	if(isNaN(deadlineDate.getTime())) return;

	let now = new Date();
	let diffDays = (deadlineDate - now) / (1000 * 60 * 60 * 24);

	if (diffDays < 2) {
		task.classList.add("deadline-soon");
	}
});












































