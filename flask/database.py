import pyrebase
import json

from flask import json

# https://github.com/thisbejim/Pyrebase/issues/294
# Monkey patch pyrebase: replace quote function in pyrebase to workaround a bug.
# See https://github.com/thisbejim/Pyrebase/issues/294.
pyrebase.pyrebase.quote = lambda s, safe=None: s

# Monkey patch pyrebase: the Storage.get_url method does need quoting :|
def get_url(self, token=None):
    path = self.path
    self.path = None
    if path.startswith('/'):
        path = path[1:]
    if token:
        return "{0}/o/{1}?alt=media&token={2}".format(self.storage_bucket, quote(path, safe=''), token)
    return "{0}/o/{1}?alt=media".format(self.storage_bucket, quote(path, safe=''))

pyrebase.pyrebase.Storage.get_url = lambda self, token=None: \
    get_url(self, token)

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

    def insert_menu(self, name, restaurant_name, menudata, img_path):
        menu_info = {
            "name": name,
            "restaurant_name" : restaurant_name,
          #  "name" : menudata['name'],
            "price" : menudata['price'],
            "allergy" : menudata['allergy'],
            "write" : menudata['write'],
            "img_path": img_path
        }
        if self.menu_duplicate_check(name, restaurant_name):
            self.db.child("menu").push(menu_info)
            print(menudata, img_path)
            return True
        else:
            return False
    
    def menu_duplicate_check(self, name, restaurant_name):
        menus = self.db.child("menu").get()
        
        if str(menus.val()) == "None":
            return True
        else:
           
            for me in menus.each():
                value = me.val()
            #    if value['name'] == name:
                if value['name'] == name and value['restaurant_name'] == restaurant_name:
                    
             #   if me.key() == name and menudata['restaurant_name']== restaurant_name:
                    return False
            return True 

    def restaurant_duplicate_check(self, name):
        restaurants = self.db.child("restaurant").get()

        if str(restaurants.val()) == "None":
            return True
        else:
            for res in restaurants.each():
                value = res.val()

                if value['name'] == name:
                    return False
            return True

    
    def get_restaurants(self):
        data = self.db.child("restaurant").order_by_child("name").limit_to_first(1000000).get().val()
        if data is None:
            return []

        return list(data.values())

    def get_home_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        return restaurants

    def get_restaurants_bycategory(self, category):
        data = self.db.child("restaurant").order_by_child("name").order_by_child("category").equal_to(category).limit_to_first(1000000).get().val()
        if data is None:
            return []

        return list(data.values())

    def get_restaurant_byname(self, name):
        restaurants = self.db.child("restaurant").get()
        target_value = None
        for res in restaurants.each():
            value = res.val()
            if value['name'] == name:
                target_value = value
        return target_value

    def insert_review(self, user, review_data, img_path):
        restaurant_name = review_data['res_name']

        review_info = {
            "user_id": user['id'],
            "user_nickname": user['nickname'],
            "res_name": restaurant_name,
            "star": review_data['star_rating'],
            "review": review_data['review'],
            "img_path": img_path,
           # "created_at": datetime.now()
        }
        self.db.child("review").push(review_info)

        # update average rate
        review_average = self.get_avgrate_by_res_name(restaurant_name)
        restaurant = self.db.child("restaurant").order_by_child("name").equal_to(restaurant_name).limit_to_first(1).get().val()
        key = list(restaurant.keys())[0]
        self.db.child("restaurant").child(key).update({"review_average": review_average})

        return True

    def get_avgrate_by_res_name(self, res_name):
        reviews = self.db.child("review").get()
        rates = []
        for review in reviews.each():
            value = review.val()
            if value['res_name'] == res_name:
                rates.append(float(value['star']) if value['star'] != '' else 0)
        return 0 if len(rates) == 0 else round(sum(rates) / len(rates), 1)

    def list_reviews(self, res_name, order="latest"):
        # NOTE: https://github.com/thisbejim/Pyrebase/issues/317
        data = self.db.child("review").order_by_child("res_name").equal_to(res_name).limit_to_first(1000000).get().val()

        if data is None:
            return []

        if order == 'good':
            reviews = dict(sorted(data.items(), key=lambda x: x[1]['star'], reverse=True))
        elif order == 'bad':
            reviews = dict(sorted(data.items(), key=lambda x: x[1]['star'], reverse=False))
        else:
            reviews = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))

        return list(reviews.values())
    
    def get_food_byname(self, name):
        restaurants = self.db.child("menu").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            print(value)

            if value['restaurant_name'] == name:
                target_value.append(value)
        return target_value

    def get_reviews(self, limit):
        data = self.db.child("review").order_by_key().limit_to_last(limit).get().val()
        reviews = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))
        return list(reviews.values())
    
    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'],
            "pw": pw,
            "nickname": data['nickname']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False
        
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        
        print("users###", users.val())
        if str(users.val()) == "None": #dataX 첫 등록 시 중복체크 로직 안타게 변경
            return True
        else:
            for res in users.each():
                value = res.val()
                
                if value['id'] == id_string:
                    return False
            return True

    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
            
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        
        return False

    def get_user(self, user_id):
        data = self.db.child("user").order_by_child("id").equal_to(user_id).get().val()
        if not data:
            return None

        user = list(data.values())

        return user[0]

    def get_user_favorites(self, user_id):
        user = self.get_user(user_id)
        if user == None:
            return []

        return user['favorites'] if 'favorites' in user else []

    def add_to_favorite(self, user_id, restaurant_name):
        user = self.db.child("user").order_by_child("id").equal_to(user_id).limit_to_first(1).get().val()
        if not user:
            return

        key = list(user.keys())[0]

        favorites = []
        if 'favorites' in user[key]:
            favorites = user[key]['favorites']
        if restaurant_name not in favorites:
            favorites.append(restaurant_name)

        self.db.child("user").child(key).update({ "favorites": favorites })

    def remove_from_favorite(self, user_id, restaurant_name):
        user = self.db.child("user").order_by_child("id").equal_to(user_id).limit_to_first(1).get().val()
        if not user:
            return

        key = list(user.keys())[0]

        favorites = []
        if 'favorites' in user[key]:
            favorites = user[key]['favorites']
        if restaurant_name in favorites:
            favorites.remove(restaurant_name)

        self.db.child("user").child(key).update({ "favorites": favorites })