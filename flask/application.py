from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
import hashlib
import math

application = Flask(__name__)
application.config["SECRET_KEY"] = "anything-you-want"

DB = DBhandler()

@application.route("/")
def hello():
    limit=9
    data = DB.get_home_restaurants()

    total=len(data)
    
    if total>=9:
        keys=(list(data))[::-1][:9]
    else:
        keys=(list(data))[::-1]
    
    print(total)
    
    datas = [data[k] for k in keys]

    reviews = DB.get_reviews(limit)
    
    return render_template(
        "index.html",
        # datas = data.items(),
        datas = datas,
        for_len = range(len(keys)),
        reviews = reviews
    )


@application.route("/favorite", methods=['GET'])
def user_favorite():
    if session.get('id') == None:
        return redirect(url_for("view_login"))

    favorites = DB.get_user_favorites(session['id'])

    restaurants = []
    if len(favorites) > 0:
        restaurants = DB.get_restaurants()

    result = []
    for restaurant in restaurants:
        if restaurant['name'] in favorites:
            result.append(restaurant)

    return render_template(
        "favorite.html",
        restaurants=result)

@application.route("/favorite", methods=['POST'])
def favorite():
    DB.add_to_favorite(session['id'], request.form['restaurant_name'])
    return jsonify(success=True)

@application.route("/unfavorite", methods=['POST'])
def unfavorite():
    DB.remove_from_favorite(session['id'], request.form['restaurant_name'])
    return jsonify(success=True)

@application.route("/login")
def view_login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_, pw_hash):
        session['id']=id_
        return redirect(url_for('list_restaurants'))
    else:
        flash("아이디 또는 비밀번호가 틀렸습니다.")
        return render_template("login.html")

@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('list_restaurants'))
    
@application.route("/signup")
def view_signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("이미 존재하는 아이디입니다.")
        return render_template("signup.html")

@application.route("/dinerform")
def view_dinerform():
    return render_template("dinerform.html")

@application.route("/dinerlist")
def view_dinerlist():
    # return render_template("dinerlist.html")
    return redirect(url_for('list_restaurants'))

@application.route("/placeDashboard")
def view_placeDashboard():
    return render_template("placeDashboard.html")

@application.route("/review_upload")
def view_reviewupload():
    return render_template("review_form.html")

@application.route("/Menu")
def view_Menu():
    return render_template("Menu.html")

@application.route("/Menu_rg", methods=['POST'])
def reg_menu():
    data=request.form
    print(data)
    return render_template("Menu_rg.html", data=data)

@application.route("/submit_diner")
def reg_diner_submit():
    name=request.args.get("name")
    addr=request.args.get("addr")
    tel=request.args.get("tel")
    category=request.args.get("category")
    price=request.args.get("price")
    park=request.args.get("park")
    time1=request.args.get("time1")
    time2=request.args.get("time2")
    site=request.args.get("site")
    file=request.args.get("file")
    
    print(name,addr,tel,category,price,park,time1,time2,site, file)


@application.route("/submit_diner_post", methods=['POST'])
def reg_diner_submit_post():
    global idx
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_restaurant(data['name'], data, image_file.filename):
        return render_template("submit_diner_result.html", data=data, image_path="static/image/"+image_file.filename)
    else:
        flash("Restaurant name already exist!")
        return redirect(url_for('view_dinerform'))


@application.route("/submit_menu")
def reg_menu_submit():
    name=request.args.get("name")
    price=request.args.get("price")
    allergy=request.args.get("allergy")
    write=request.args.get("write")
    file=request.args.get("file")
    
    print(name,price,allergy,write,file)

@application.route("/submit_menu_post", methods=['POST'])
def reg_menu_submit_post():
    global idx
    data = request.form
    # print(data)
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    menudata=request.form
  #  if DB.insert_menu(menudata['name'], menudata, image_file.filename):
    if DB.insert_menu(menudata['name'], menudata['restaurant_name'], menudata, image_file.filename):
        return render_template("submit_menu_result.html", menudata=menudata, image_path="static/image/"+image_file.filename)
    else:
        flash("Menu name already exist!")
        return render_template("Menu_rg.html", data=data)

@application.route("/list")
def list_restaurants():
    page = request.args.get("page", 0, type=int)
    category = request.args.get("category", "all")
    limit = 9
    
    start_idx = limit*page
    end_idx = limit*(page+1)

    if category == "all":
        data = DB.get_restaurants()
    else:
        data = DB.get_restaurants_bycategory(category)

    tot_count = len(data)
    data = data[start_idx:end_idx]
    page_count = math.ceil(tot_count/9)
    # real_url = "http://ewhafood.run.goorm.io/list?page="+str(page_count-1)
    # print(real_url)
    
    return render_template(
        "list.html",
        datas = data,
        total = tot_count,
        limit = limit,
        page = page,
        page_count = math.ceil(tot_count/9),
        category=category,
        real_url = "http://ewhafood.run.goorm.io/list?page="+str(page_count-1)
        # real_page_count = str(int((tot_count/9)))
    )

@application.route("/view_detail/<name>/")
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))
    if data is None:
        print("restaurant not found")

    review = DB.list_reviews(str(name))
    rAmount = len(review)
    menudata = DB.get_food_byname(str(name))
    tot_count = len(menudata)

    favorited = False
    if session.get('id'):
        favorites = DB.get_user_favorites(session['id'])
        favorited = str(name) in favorites

    return render_template("detail.html",
                           data = data,
                           review = review[0:2],
                           menudata = menudata,
                           rAmount = rAmount,
                           total = tot_count,
                           favorited = favorited)

@application.route("/review/<res_name>/")
def restaurant_review(res_name):
    order = request.args.get("order", "latest")
    review_data = DB.list_reviews(str(res_name), order)
    restaurant = DB.get_restaurant_byname(str(res_name))
    print("####data:",review_data)
    return render_template("review.html",
                           restaurant = restaurant,
                           review_data = review_data,
                           order=order)

@application.route("/restaurants/<res_name>/new", methods=['GET'])
def new_restaurant_review(res_name):
    if session.get('id') == None:
        return redirect(url_for("view_login"))

    return render_template("review_form.html", res_name=res_name)

@application.route("/restaurants/<res_name>/review", methods=['POST'])
def create_review(res_name):
    image_file = request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    review_data = request.form
    user = DB.get_user(session['id'])

    if DB.insert_review(user, review_data, image_file.filename):
        return redirect(url_for('restaurant_review', res_name=res_name))
    
    
@application.route("/menu_list/<restaurant_name>/")
def view_foods(restaurant_name):
    
    data = DB.get_food_byname(str(restaurant_name))
    tot_count = len(data)
    page_count = len(data)

    return render_template(
        "menu_list.html",
        datas=data,
        total=tot_count,
        restaurant_name = restaurant_name
    )

    if DB.insert_review(review_data, image_file.filename):
        return redirect(url_for('restaurant_review', res_name=res_name))

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)