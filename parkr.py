from flask import Flask, render_template
from utility import get_nodes, get_edges


app = Flask(__name__)


@app.route('/')
def index():
    nodes = get_nodes()
    block_names = nodes['block_name']
    return render_template('index.html', title='Test title', blocks=block_names)







if __name__ == '__main__':
    app.run(debug=True)