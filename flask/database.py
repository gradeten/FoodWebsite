import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)
            
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def insert_restaurant(self, name, data, img_path):
        restaurant_info = {
            "name": name,
            "addr": data['addr'],
            "tel": data['tel'],
            "category": data['category'],
            "price": data['price'],
            "park": data['park'],
            "time1": data['time1'],
            "time2": data['time2'],
            "site": data['site'],
            "img_path": img_path
        }
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").push(restaurant_info)
            print(data, img_path)
            return True
        else:
            return False

    def insert_menu(self, name, menudata, img_path):
        menu_info = {
            "restaurant_name" : menudata["restaurant_name"],
            "name" : menudata['name'],
            "price" : menudata['price'],
            "allergy" : menudata['allergy'],
            "write" : menudata['write'],
            "img_path": img_path
        }
        if self.menu_duplicate_check(name):
            self.db.child("menu").child(name).set(menu_info)
            print(menudata, img_path)
            return True
        else:
            return False
       
    def menu_duplicate_check(self, name):
        menus = self.db.child("menu").get()
        
        if str(menus.val()) == "None":
            return True
        else:
            for me in menus.each():
                if me.key() == name:
                    return False
            return True   

    def restaurant_duplicate_check(self, name):
        restaurants = self.db.child("restaurant").get()
        for res in restaurants.each():
            value = res.val()
            
            if value['name'] == name:
                return False
        return True
    
    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        return restaurants
    
    def get_restaurant_byname(self, name):
        restaurants = self.db.child("restaurant").get()
        target_value = ""
        for res in restaurants.each():
            value = res.val()
            
            if value['name'] == name:
                target_value = value
        return target_value

    def insert_review(self, review_data, img_path):
        review_info = {
            "res_name": review_data['res_name'],
            "star": review_data['star_rating'],
            "review": review_data['review'],
            "img_path": img_path,
           # "created_at": datetime.now()
        }
        self.db.child("review").push(review_info)
        print(review_data, img_path)
        return True

    def get_avgrate_by_res_name(self, res_name):
        reviews = self.db.child("review").get()
        rates = []
        for review in reviews.each():
            value = review.val()
            if value['res_name'] == res_name:
                rates.append(float(value['star']) if value['star'] != '' else 0)
        return 0 if len(rates) == 0 else round(sum(rates) / len(rates), 1)

    def get_review_by_res_name(self, res_name):
        reviews = self.db.child("review").get()
        target_value = []
        for review in reviews.each():
            value = review.val()
            if value['res_name'] == res_name:
                target_value.append(value)
        return target_value
    
    
    def get_food_byname(self, name):
        restaurants = self.db.child("menu").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            print(value)

            if value['restaurant_name'] == name:
                target_value.append(value)
        return target_value    