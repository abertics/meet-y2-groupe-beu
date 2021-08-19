from flask import Flask, render_template, request, redirect, make_response
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'

# TODO: Add all of the routes you want below this line!

@app.route("/")
def index():
    if request.cookies.get('userId') != None :
        return render_template("index.html", posts = get_posts(), User = get_user_by_id(request.cookies.get("userId")), get_user_by_name = get_user_by_name)
    else:
        return render_template("index.html", posts = get_posts(), get_user_by_name = get_user_by_name)

@app.route("/about-us")
def about():
    return render_template("about_us.html", User = get_user_by_id(request.cookies.get('userId')))

@app.route('/profile/<int:userId>')
def profile(userId):
    if str(userId) == str(request.cookies.get('userId')):
        return redirect('/edit_user')
    else : 
        return render_template("profile.html", User = get_user_by_id(request.cookies.get('userId')), profile= get_user_by_id(userId))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        nickname = request.form['nickname']
        password = request.form['password']
        user = get_user_by_name(nickname)
        if user and user.password == password:
            response = make_response(render_template("index.html", posts = get_posts(), User = get_user_by_name(nickname), get_user_by_name = get_user_by_name))
            response.set_cookie(key='userId', value=str(get_user_by_name(nickname).id))
            return response
        else:
            return redirect('/tryagain')


@app.route('/signup', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template('signup.html', User = get_user_by_id(request.cookies.get('userId')))
    else:
        nickname = request.form['nickname']
        password = request.form['password']
        bio = request.form['bio']
        age = request.form['age']
        profile_picture_link = request.form['profile_picture_link']
        nickname = sign_up(nickname, password, bio, age, profile_picture_link)
        response = make_response(render_template("index.html", posts = get_posts(), User = get_user_by_name(nickname), get_user_by_name = get_user_by_name))
        response.set_cookie(key='userId', value=str(get_user_by_name(nickname).id))
        return response

@app.route('/create', methods=['GET', 'POST'])
def createPost():
    if request.method == 'GET':
        if request.cookies.get('userId'):
            return render_template('create.html', User = get_user_by_id(request.cookies.get('userId')))
        else :
            return redirect('/tryagain')
    else :
        post_a_post(get_user_by_id(request.cookies.get('userId')).nickname, request.form['content'], request.form['picture'], "")
        return redirect('/')

@app.route('/post/<int:postId>', methods=['GET', 'POST'])
def commentPost(postId):
    if request.method == 'GET':
        if request.cookies.get('userId'):
            return render_template('post.html', User= get_user_by_id(request.cookies.get('userId')), post = get_post_by_id(postId), comments = get_comments(postId), get_user_by_name = get_user_by_name)
        else :
            return redirect('/tryagain')
    else : 
        add_comment(postId, request.form['comment'])
        return redirect('/post/'+ str(postId))

@app.route('/signout')
def signout():
    response = make_response(render_template("index.html", posts = get_posts(), User = None, get_user_by_name = get_user_by_name))
    response.set_cookie('userId', value= '' ,expires=0)
    return response

@app.route('/edit_user', methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        if request.cookies.get('userId'):
            return render_template('edit_user.html', User = get_user_by_id(request.cookies.get('userId')))
        else :
            return redirect('/tryagain')
    else:
        edit_account(get_user_by_id(request.cookies.get('userId')).nickname, request.form['nickname'], request.form['password'], request.form['bio'], request.form['age'], request.form['profile_picture_link'])
        return redirect('/profile/' + request.cookies.get('userId'))

@app.route("/edit_post/<int:postId>", methods=['GET', 'POST'])
def editPost(postId):
    if request.method == 'GET':
        if get_post_by_id(postId).nickname == get_user_by_id(request.cookies.get('userId')).nickname:
            return render_template('edit_post.html', Post = get_post_by_id(postId), User=get_user_by_id(request.cookies.get('userId')))
        else : 
            return redirect('/tryagain')
    else:
        if get_post_by_id(postId).nickname == get_user_by_id(request.cookies.get('userId')).nickname:
            content = request.form['content']  
            picture = request.form['picture']
            recreate_post(postId, content, picture)  
            return redirect('/')
        else:
            return redirect('/tryagain')

@app.route("/tryagain")
def tryagain():
    return render_template("tryagain.html")

@app.route("/delete")
def delete():
    posts = get_posts_by_name(get_user_by_id(request.cookies.get('userId')).nickname)
    for i in posts:
        delete_post(i.id)
    delete_user(request.cookies.get('userId'))
    return signout()

@app.route("/delete_post/<int:postId>")
def deletePost(postId):
    if request.method == 'GET':
        if get_post_by_id(postId).nickname == get_user_by_id(request.cookies.get('userId')).nickname:
            delete_post(postId)
            return redirect('/')
        else : 
            return redirect('/tryagain')

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
