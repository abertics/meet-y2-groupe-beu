from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
import json, requests, random

engine = create_engine('sqlite:///database.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

NULL = 0

def get_user_by_name(nickname):
	user = session.query(User).filter_by(nickname = nickname).first()
	return user

def sign_up(nickname, password, bio, age, profile_picture_link):
	user_ = get_user_by_name(nickname)
	if user_ != None:
		return "You used an exists username.. Try again"

	if len(nickname) == NULL:
		response = requests.get("https://dog.ceo/api/breeds/list/all")
		json_string = response.content
		parsed_json = json.loads(json_string)
		names = parsed_json["message"]
		list_of_names = []
		for name in names.keys():
			list_of_names.append(name)
		# gets random number
		i = random.randint(0,len(list_of_names))
		nickname = list_of_names[i]

	if len(profile_picture_link) == NULL:
		response = requests.get("https://randomfox.ca/floof/")
		json_string = response.content
		parsed_json = json.loads(json_string)
		profile_picture_link = parsed_json["image"]

	user = User(nickname = nickname, 
		password = password, 
		bio = bio, 
		age = age, 
		profile_picture_link = profile_picture_link)
	session.add(user)
	session.commit()
	return nickname

def get_posts():
	return session.query(Post).all()

def get_users():
	users = session.query(User).all()
	return users

def delete_user(id):
	session.query(User).filter_by(id = id).delete()
	session.commit()

def post_a_post(nickname, content, image_link, comments):
	user_ = get_user_by_name(nickname)
	if user_ == None:
		return "You can't post a post without a user.. sign up please"
	post = Post(nickname = nickname, 
		content = content, 
		image_link = image_link, 
		comments = comments)
	session.add(post)
	session.commit()

def get_post_by_id(id):
	post = session.query(Post).filter_by(id = id).first()
	return post

def get_user_by_id(id):
	user = session.query(User).filter_by(id = id).first()
	return user

def delete_post(id):
	session.query(Post).filter_by(id = id).delete()
	session.commit()

def add_comment(id, comment):
	post = get_post_by_id(id)
	if post.comments == "":
		post.comments += comment
	else:
		post.comments += "|" + comment
	session.commit()

def get_comments(post_id):
	post = get_post_by_id(post_id)
	comments = post.comments
	comments = list(comments.split('|'))
	return comments

def edit_account(pervious_name, nickname, password, bio, age, profile_picture_link):
	user = session.query(User).filter_by(nickname = pervious_name).first()
	previous_details = [user.nickname, user.password, user.bio, user.age, user.profile_picture_link]
	new_details = [nickname, password, bio, age, profile_picture_link]
	final_details = []
	for i in range(len(new_details)):
		if len(str(new_details[i])) > 0:
			final_details.append(new_details[i])
		else:
			final_details.append(previous_details[i])
	user.nickname = final_details[0]
	user.password = final_details[1]
	user.bio = final_details[2]
	user.age = final_details[3]
	user.profile_picture_link = final_details[4]
	session.commit()

def recreate_post(post_id, content, image_link):
	post = session.query(Post).filter_by(id = post_id).first()
	previous_details = [post.content, post.image_link]
	new_details = [content, image_link]
	final_details = []
	for i in range(len(new_details)):
		if len(str(new_details[i])) > 0:
			final_details.append(new_details[i])
		else:
			final_details.append(previous_details[i])
	post.content = final_details[0]
	post.image_link = final_details[1]
	session.commit()

def get_posts_by_name(nickname):
	return session.query(Post).filter_by(nickname = nickname).all()