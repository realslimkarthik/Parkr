from flask import Flask, render_template, request, jsonify
from utility import get_nodes, get_edges, get_node_id_from_name, convert_to_datetime_duplicate
from algorithms import simulate


app = Flask(__name__)


@app.route('/')
def index():
    nodes = get_nodes()
    block_names = nodes['block_name']
    return render_template('index.html', title='Enter your destination', blocks=block_names)



@app.route('/get_spot')
def get_spot():
	origin = request.args.get('origin','')
	destination = request.args.get('destination','')
	time = request.args.get('time','')
	#algorithm = request.args.get('algorithm','')
	route_result1 = simulate(get_node_id_from_name(origin), get_node_id_from_name(destination),convert_to_datetime_duplicate(time),'p',0)
	route_result1['distance'] = str(route_result1['distance'])
	route_result1['walking_distance'] = str(route_result1['walking_distance'])
	route_result1['time'] = str(route_result1['time'])
	route_result1['running_time'] = str(route_result1['running_time'])

	route_result2 = simulate(get_node_id_from_name(origin), get_node_id_from_name(destination),convert_to_datetime_duplicate(time),'d',0)
	route_result2['distance'] = str(route_result2['distance'])
	route_result2['walking_distance'] = str(route_result2['walking_distance'])
	route_result2['time'] = str(route_result2['time'])
	route_result2['running_time'] = str(route_result2['running_time'])

	return jsonify(dict([('p',route_result1), ('d',route_result2)]))




if __name__ == '__main__':
    app.run(debug=True)
