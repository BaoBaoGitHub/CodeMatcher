from flask import Flask,url_for,request,render_template

app  =  Flask(__name__)
@app.route('/index', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        '''
        if request.form['user'] == 'admin':
            return 'Admin login successfully!'
        else:
            return 'No such user!'
        '''
        return str(request.form['user'])
    title = request.args.get('title','Default')
    return render_template('index.html', title=title)

if __name__ == "__main__":
    app.run(debug=True)