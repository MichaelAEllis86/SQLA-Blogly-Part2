from unittest import TestCase
from app import app
from flask import request
from models import db, User, connect_db

#use a test datanase and don't echo SQL give sqla context
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///test_blogly_db'
app.config['SQLALCHEMY_ECHO']= False
connect_db(app)

#create model tables in test db
db.drop_all()
db.create_all()


#todo! additional routes like edit GET and edit POST and user details need done! 
# large issue! tests are effecting the app.py database unintentionally. All tests are passing and data isn't important atm however this should be looked at.

class FlaskTests(TestCase):

    def setUp(self):
        """setup! enabling flask testing configs here and getting rid of flask DB TB during testing. Delete all old entries from test database, add a test user as a test reference point for each test"""
        app.config['TESTING']=True
        app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar']

        #dblogic

        User.query.delete()
        user=User(first_name="test", last_name="testuser", image_url="https://static.wikia.nocookie.net/spsot/images/7/73/Ic_unlock_cpm_shoe.png/revision/latest?cb=20150112020641")
        db.session.add(user)
        db.session.commit()

        self.user=user
        self.id = user.id
        self.first_name = user.first_name
        self.last_name= user.last_name

        print(f"printing the test user {user}")
        print(f"printing the test user.id {user.id}")
        print(f"printing the test user.first_name {user.first_name}")
        print(f"printing the test user.last_name {user.last_name}")
    
    
    def tearDown(self):
        db.session.rollback()


    
    def test_base_page(self):
        """Test if root page returns correct status code for GET request and returns included html"""
        with app.test_client() as client:
            response=client.get("/")
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn('<h1 id="basewelcome"> Welcome to Blogly Part1 &#127876 Happy 2024! &#127878</h1>',html)
    
    def test_new_user_form_page(self):
        """Test if new_user form page returns correct status code for GET request and returns included html"""
        with app.test_client() as client:
            response=client.get("/users/new")
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn('<h1>Create a User</h1>',html)

    
    def test_new_user_post(self):
        """Test if new_user form submit returns correct status code for redirect and redirects to correct location"""
        with app.test_client() as client:
            response=client.post("/users/new", data={'first_name':'sphinx', 'last_name':'thecat','image_url':'https://lh3.googleusercontent.com/pw/ABLVV84DKj-7lYUSIYNzwyAzvCFeNNIxlZ1UGLcrtek8Kn5mMooP68XpWS4NDcAEV2ydx5S7Cs7hwOhTZrQDlQ_SYrKF1kgJ8cLKWC-qIfbQruhb0YKlqRqOULi_DvBY8OiIj7pNpsgthPpGt4g0caMkY4MmCdewn-qlh_O4oI6XJTnZ4LpsWlCvdjomLy8KAuhqHgfKph4ioZLeRpwU8QTihmg91lmX1zHM0va92ulSeGJXwg1FkYu55ZeohYg5_ql0HeBSE6eFjJSNdVjchrP38PIHs4ixKvlE8csxYEKRfw6s703c5ukODmaXibw4CHsZFrDyIQuL3iiGWtIsh8qwSG6YlwBCYRyL7GhCy0krJkMKYMmLzyhHbBetECIrnA-ZhPtuv4knTxqOcNjqO5VbTkK4oKLZgQfn5dCu6BtRgQW1rK5z2cNOX3tG30CKX4ED9magN1WRtktnl4W-fYGKgsVeydPhi0FWMFdfpQ22w2m3C9kIpgy-L7B9FcuAdlBaGl-zH1lvp8nC5AgUiOdeksp9roas5jWGhwvC1BihOZYyCUYRfZKTGaoHMHfLpzAzL_0YKdqIF2CNctf-yHFrFfRULw39ceHh5HzSfQZ8O0qYDh6G801ssImwqulmKmk0dRuDgZXNgYE32p2WGpRu7lhFJ8Pxin037V3w6-zClnXM1-8u4tpjT2gWoNxMdT-rgvFF-qjCY_PkQeKEETaL8lzTsD46oZTTyO0cgm96ERXa-6sZKZyKgMsUZUw9PpZag6jYMc342n8l6y_KVYK6a8yfU22o6w9lGiiSaJOTf5TLlENpFskDN-NK0bkxXE1hoTC0Gp8NcpPZxNz9nnVBwN7qJsyedDnC8EY0WOaDJK8zkXpGoC5ZQZvq5pZtbdKtAvjCQx_moEGIe_2d7l88G7KvkTkmrSXZdxU-Vw4NGcc38yP83KzgKRj9FJpILlFW5Hj6Fuo-I-d4WeKnkIZrkGmqZd5s14I=w200-h200-s-no-gm?authuser=0'})
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,302)
            self.assertIn(response.location,"/users")
        
    def test_new_user_post_redirect(self):
        """Test if converter form page submit returns correct status code and html after full redirect and proper flash message response"""
        with app.test_client() as client:
            response=client.post("/users/new", follow_redirects=True, data={'first_name':'sphinx', 'last_name':'thecat','image_url':'https://lh3.googleusercontent.com/pw/ABLVV84DKj-7lYUSIYNzwyAzvCFeNNIxlZ1UGLcrtek8Kn5mMooP68XpWS4NDcAEV2ydx5S7Cs7hwOhTZrQDlQ_SYrKF1kgJ8cLKWC-qIfbQruhb0YKlqRqOULi_DvBY8OiIj7pNpsgthPpGt4g0caMkY4MmCdewn-qlh_O4oI6XJTnZ4LpsWlCvdjomLy8KAuhqHgfKph4ioZLeRpwU8QTihmg91lmX1zHM0va92ulSeGJXwg1FkYu55ZeohYg5_ql0HeBSE6eFjJSNdVjchrP38PIHs4ixKvlE8csxYEKRfw6s703c5ukODmaXibw4CHsZFrDyIQuL3iiGWtIsh8qwSG6YlwBCYRyL7GhCy0krJkMKYMmLzyhHbBetECIrnA-ZhPtuv4knTxqOcNjqO5VbTkK4oKLZgQfn5dCu6BtRgQW1rK5z2cNOX3tG30CKX4ED9magN1WRtktnl4W-fYGKgsVeydPhi0FWMFdfpQ22w2m3C9kIpgy-L7B9FcuAdlBaGl-zH1lvp8nC5AgUiOdeksp9roas5jWGhwvC1BihOZYyCUYRfZKTGaoHMHfLpzAzL_0YKdqIF2CNctf-yHFrFfRULw39ceHh5HzSfQZ8O0qYDh6G801ssImwqulmKmk0dRuDgZXNgYE32p2WGpRu7lhFJ8Pxin037V3w6-zClnXM1-8u4tpjT2gWoNxMdT-rgvFF-qjCY_PkQeKEETaL8lzTsD46oZTTyO0cgm96ERXa-6sZKZyKgMsUZUw9PpZag6jYMc342n8l6y_KVYK6a8yfU22o6w9lGiiSaJOTf5TLlENpFskDN-NK0bkxXE1hoTC0Gp8NcpPZxNz9nnVBwN7qJsyedDnC8EY0WOaDJK8zkXpGoC5ZQZvq5pZtbdKtAvjCQx_moEGIe_2d7l88G7KvkTkmrSXZdxU-Vw4NGcc38yP83KzgKRj9FJpILlFW5Hj6Fuo-I-d4WeKnkIZrkGmqZd5s14I=w200-h200-s-no-gm?authuser=0'},)
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn('<h3>Users list</h3>',html)
            self.assertIn('<p class="message">message: new user created!!</p>',html)

    def test_users_page(self):
        """Test if users page returns correct status code for GET request and returns included html, tests if test user is used to create the user detail link"""
        with app.test_client() as client:
            response=client.get("/users")
            html=response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn('<h3>Users list</h3>',html)
            self.assertIn(f'<a href="/users/{self.id}">{self.first_name} {self.last_name}</a>',html)
    
