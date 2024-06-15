from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de tareas (simulada)
tasks = [
    {"id": 1, "title": "Hacer la compra", "description": "Comprar víveres para la semana", "completed": False}
]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "description": data["description"],
        "completed": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        data = request.json
        task["title"] = data["title"]
        task["description"] = data["description"]
        task["completed"] = data["completed"]
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
