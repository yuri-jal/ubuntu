from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

#Flask instance make
app = Flask(__name__)
api = Api(app)

#todo list
TODOS = {
	'todo1':{'task': 'Make Money'},
	'todo2':{'task': 'Play PS4'},
	'todo3':{'task': 'Study!'},
}

#exception handling
def abort_if_todo_doesnt_exist(todo_id):
	if todo_id not in TODOS:
		abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

#todo
#Get, Delete, Put definition
class Todo(Resource):
	def get(self, todo_id):
	    abort_if_todo_doesnt_exist(todo_id)
	    return TODOS[todo_id]

	def delete(self, todo_id):
	    abort_if_todo_doesnt_exist(todo_id)
	    del TODOS[todo_id]
	    return '', 204
	
	def put(self, todo_id):
	    args = parser.parse_args()
	    task = {'task': args['task']}
	    TODOS[todo_id] = task
	    return task, 201

#TODO LIST	
#Get POST Definition
class TodoList(Resource):
	def get(self):
		return TODOS
	def post(self):
		args = parser.parse_args()
		todo_id = 'todo%d' % (len(TODOS) + 1)
		TODOS[todo_id] = {'task': args['task']}
		return TODOS[todo_id], 201

##
## URL Router mapping(rest url definition)
##
api.add_resource(TodoList, '/todos/')
api.add_resource(Todo, '/todos/<string:todo_id>')

#server execution
if __name__=='__main__':
	app.run(debug=True)
