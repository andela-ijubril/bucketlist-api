from flask import Flask, jsonify, abort
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


@app.route('/auth/login')
def login():
    return "Login Successful"


@app.route('/auth/logout')
def logout():
    return "Logout Successful"


@app.route('/auth/register')
def register():
    return "Registration Successful"


@app.route('/bucketlists')
def create_bucketlist():
    return jsonify({'bucketlists': bucketlists})
    # return "Bucket List created and can also be listed Successfully"


@app.route('/bucketlists/<int:id>/')
def get_bucket(id):
    bucketlist = [bucketlist for bucketlist in bucketlists if bucketlist['id'] == id]
    if len(bucketlist) == 0:
        abort(404)
    return jsonify({'bucketlist': bucketlist[0]})
    # GET, PUT, DELETE
    # Confirm Whether integer can also be formatted with %s


@app.route('/bucketlists/<int:id>/items')
def add_a_new_item_to_bucketlist(id):
    return "Successfully Added item to the bucketlist %s" % id


@app.route('/bucketlists/<int:id>/items/<int:item_id>')
def get_this_item_in_the_bucket_list(id, item_id):
    return "%s Is currently in the bucketlists %s" % (item_id, id)


@app.route('/bucketlists/<string:search>')
def search_for_item_in_bucket_list(search):
    return "The item ", search, " is in teh list"


@app.route('/bucketlists/<int:id>')
def limit_api_record(id):
    return "WE are going to limit response by ", id, " records"


if __name__ == '__main__':
    app.run(debug=True)
