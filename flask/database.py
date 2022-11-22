import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
            
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def insert_restaurant(self, name, data, img_path):
        restaurant_info = {
            "addr": data['addr'],
            "tel": data['tel'],
            "category": data['category'],
            "park": data['park'],
            "time1": data['time1'],
            "time2": data['time2'],
            "site": data['site'],
            "img_path": img_path
        }
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").child(name).set(restaurant_info)
            print(data,img_path)
            return True
        else:
            return False
        
        
        
    def insert_menu(self, name, menudata, img_path):
        menu_info = {
            "price" : menudata['price'],
            "allergy" : menudata['allergy'],
            "write" : menudata['write'],
            "img_path": img_path
        }
        if self.menu_duplicate_check(name):
            self.db.child("menu").child(name).set(menu_info)
            print(menudata,img_path)
            return True
        else:
            return False
       
    def menu_duplicate_check(self,name):
        menus = self.db.child("menu").get()
        for me in menus.each():
            if me.key() == name:
                return False
        return True   
       
    
    
    def restaurant_duplicate_check(self, name):
        restaurants = self.db.child("restaurant").get()
        for res in restaurants.each():
            if res.key() == name:
                return False
        return True


    def insert_review(self,reviewdata,img_path):
        review_info ={
            "star":reviewdata['starRate'],
            "review":reviewdata['review'],
            "img_path":img_path

        }
        self.db.child("review").push(review_info)
        print(reviewdata,img_path)
        return True