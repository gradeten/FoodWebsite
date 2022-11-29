from flask import Flask, render_template, request, flash, redirect, url_for
from database import DBhandler
import sys
import math

application = Flask(__name__)
application.config["SECRET_KEY"] = "anything-you-want"

DB = DBhandler()

@application.route("/")
def hello():
    
    data = DB.get_restaurants()

    total=len(data)
    
    if total>=9:
        keys=(list(data))[::-1][:9]
    else:
        keys=(list(data))[::-1]
    
    print(total)
    
    datas = [data[k] for k in keys]
    
    return render_template(
        "index.html",
        # datas = data.items(),
        datas = datas,
        for_len = range(len(keys))
        
    )



@application.route("/favorite")
def view_favorite():
    return render_template("favorite.html")

@application.route("/login")
def view_login():
    return render_template("login.html")

@application.route("/member-join")
def view_memberjoin():
    return render_template("member-join.html")

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

@application.route("/review")
def view_review():
    return render_template("review.html")

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
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    menudata=request.form
    if DB.insert_menu(menudata['name'], menudata, image_file.filename):
        return render_template("submit_menu_result.html", menudata=menudata, image_path="static/image/"+image_file.filename)
    else:
        return "Menu name already exist!"




@application.route("/list")
def list_restaurants():
    page = request.args.get("page", 0, type=int)
    limit = 9
    
    start_idx = limit*page
    end_idx = limit*(page+1)
    data = DB.get_restaurants()
    # print(data)
    tot_count = len(data)
    # data = dict(list(data.items())[start_idx:end_idx])
    data = list(data.items())[start_idx:end_idx]
    page_count = len(data)
    
    return render_template(
        "list.html",
        # datas = data.items(),
        datas = data,
        total = tot_count,
        limit = limit,
        page = page,
        page_count = math.ceil(tot_count/9),
        real_page_count = str(int((tot_count/9)))
    )

@application.route("/view_detail/<name>/")
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))
    print("####data:", data)
    review = DB.get_review_by_res_name(str(name))
    rAmount = len(review)
    r_avg_rate = DB.get_avgrate_by_res_name(str(name))
    menudata = DB.get_food_byname(str(name))
    tot_count = len(menudata)
    
    return render_template("detail.html", data=data, review=review, r_avg_rate=r_avg_rate, menudata=menudata,
        rAmount = rAmount, total=tot_count)

@application.route("/review/<res_name>/")
def restaurant_review(res_name):
    review_data = DB.get_review_by_res_name(str(res_name))
    r_avg_rate = DB.get_avgrate_by_res_name(str(res_name))
    print("####data:",review_data)
    return render_template("review.html", res_name=res_name, review_data=review_data, r_avg_rate=r_avg_rate)

@application.route("/restaurants/<res_name>/new", methods=['GET'])
def new_restaurant_review(res_name):
    return render_template("review_form.html", res_name=res_name)

@application.route("/restaurants/<res_name>/review", methods=['POST'])
def create_review(res_name):
    image_file = request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    review_data = request.form

    if DB.insert_review(review_data, image_file.filename):
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