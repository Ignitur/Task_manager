from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
db = SQLAlchemy(app)


class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(200), nullable=False)
	description = db.Column(db.Text, nullable=True)
	status = db.Column(db.String(50), default="pending")
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	deadline = db.Column(db.DateTime, nullable=True)

	def to_dict(self):
		return {
			"id": self.id,
			"title": self.title,
			"description": self.description,
			"created_at": self.created_at.strftime("%Y-%m-%d") if self.created_at else None,
			"deadline": self.deadline.strftime("%Y-%m-%d") if self.deadline else None,
	}

with app.app_context():
	db.create_all()






@app.route("/")
def index():
	tasks = Task.query.all()
	return render_template("index.html", tasks=tasks)

@app.route("/tasks", methods=["GET"])
def get_tasks():
	tasks = Task.query.all()
	return jsonify([{
		"id": t.id, 
		"title": t.title, 
		"description": t.description, 
		"status": t.status,
		"deadline": t.deadline
		} for t in tasks])


@app.route("/tasks", methods=["POST"])
def create_task():
	data = request.get_json()
	if not data or "title" not in data:
		return jsonify({"error": "Invalid request"}), 400

	title = data["title"].strip()
	description = data.get("description", "").strip()
	status = data.get("status", "pending").strip().lower()
	deadline_str = data.get("deadline")

	try:
		deadline = datetime.strptime(deadline_str, "%Y-%m-%d") if deadline_str else None
	except ValueError:
		return jsonify({"error": "Invalid date format. use YYYY-MM-DD."}), 400

	allowed_statuses = {"pending", "in_progress", "completed"}
	if status not in allowed_statuses:
		return jsonify({"error": "Invalid status. Use one of {allowed_statuses}"}), 400

	new_task = Task(
		title=title,
		description=description,
		status=status,
		deadline=deadline
	)

	db.session.add(new_task)
	db.session.commit()

	return jsonify(new_task.to_dict()), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
	task = Task.query.get(task_id)
	if not task:
		return jsonify({"error": "Task not found"}), 404

	data = request.get_json()

	if "title" in data:
		task.title = data["title"]
	if "description" in data:
		task.description = data["description"]
	if "status" in data: 
		task.status = data["status"]
	if "deadline" in data:
		try:
			task.deadline = datetime.strptime(data["deadline"], "%Y-%m-%d")
		except ValueError:
			return jsonify({"error": "Invalid date format. use YYYY-MM-DD."}), 400

	db.session.commit()

	return jsonify ({
		"message": "Task updated", 
		"task": {
			"id": task.id, 
			"description": task.description,
			"title": task.title, 
			"status": task.status,
			"deadline": task.deadline.strftime("%Y-%m-%d") if task.deadline else None
		}
	})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
	task = Task.query.get(task_id)
	if not task:
		return jsonify({"error": "Task not found"}), 404

	db.session.delete(task)
	db.session.commit()
	return jsonify({"message": "Task deleted"})




if __name__ == "__main__":
	app.run(debug=True)



















