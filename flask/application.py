from flask import Flask, render_template, request
from database import DBhandler
import sys

application = Flask(__name__)

DB = DBhandler()

@application.route("/")
def hello():
    return render_template("index.html")

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
    return render_template("dinerlist.html")

@application.route("/placeDashboard")
def view_placeDashboard():
    return render_template("placeDashboard.html")

@application.route("/review_upload")
def view_reviewupload():
    return render_template("review_upload.html")

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
    park=request.args.get("park")
    time1=request.args.get("time1")
    time2=request.args.get("time2")
    site=request.args.get("site")
    file=request.args.get("file")
    
    print(name,addr,tel,category,park,time1,time2,site, file)


@application.route("/submit_diner_post", methods=['POST'])
def reg_diner_submit_post():
    global idx
    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_restaurant(data['name'], data, image_file.filename):
        return render_template("submit_diner_result.html", data=data, image_path="static/image/"+image_file.filename)
    else:
        return "Restaurant name already exist!"


@application.route("/submit_menu")
def reg_menu_submit():
    name=request.args.get("name")
    price=request.args.get("price")
    allergy=request.args.get("allergy")
    write=request.args.get("write")
    picture=request.args.get("file")
    
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



@application.route("/submit_review_post", methods=['POST'])
def reg_review_submit_post():

    image_file=request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    reviewdata=request.form

    if DB.insert_review(reviewdata,image_file.filename):
        return render_template("submit_review_result.html",reviewdata=reviewdata, image_path="static/image/"+image_file.filename)







if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)