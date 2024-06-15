from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class TaskService(ServiceBase):
    @rpc(Integer, _returns=Iterable(Unicode))
    def get_task(ctx, task_id):
        for task in tasks:
            if task["id"] == task_id:
                yield task

    @rpc(Integer, Unicode, Unicode, Boolean, _returns=Iterable(Unicode))
    def create_task(ctx, id, title, description, completed):
        tasks.append({"id": id, "title": title, "description": description, "completed": completed})
        yield "Task created successfully"

    @rpc(Integer, Unicode, Unicode, Boolean, _returns=Iterable(Unicode))
    def update_task(ctx, task_id, title, description, completed):
        for task in tasks:
            if task["id"] == task_id:
                task["title"] = title
                task["description"] = description
                task["completed"] = completed
                yield "Task updated successfully"
        yield "Task not found"

    @rpc(Integer, _returns=Iterable(Unicode))
    def delete_task(ctx, task_id):
        global tasks
        tasks = [task for task in tasks if task["id"] != task_id]
        yield "Task deleted successfully"

tasks = [
    {"id": 1, "title": "Hacer la compra", "description": "Comprar víveres para la semana", "completed": False}
]

application = Application([TaskService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
