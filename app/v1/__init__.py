from app.v1.views import products_view,service, auth
from flask import Blueprint
my_v1 = Blueprint('my_v1', __name__)
my_v1.add_url_rule('/signup', view_func=auth.signup, methods=['POST'])
my_v1.add_url_rule('/login', view_func=auth.login, methods=['POST'])
my_v1.add_url_rule('/get_users', view_func=auth.get_users, methods=['GET'])
my_v1.add_url_rule('/create_admin', view_func=auth.make_admin, methods=['PATCH'])
my_v1.add_url_rule('/confirm_email/<token>/<email>', view_func=auth.confirm_email, methods=['POST'])
my_v1.add_url_rule('/forgot_password', view_func=auth.forgot_password, methods=['POST'])
my_v1.add_url_rule('/recover_account/<token>/<email>', view_func=auth.recover_account, methods=['POST','GET'])
my_v1.add_url_rule('/change_password', view_func=auth.change_password, methods=['POST'])
my_v1.add_url_rule('/user_info_update', view_func=auth.user_update_info, methods=['PATCH'])
my_v1.add_url_rule('/User/<int:userid>', view_func=auth.get_single_user, methods=['GET'])

# product blueprints
my_v1.add_url_rule('/add_project', view_func=products_view.createproduct, methods=['POST'])
my_v1.add_url_rule('/all_products', view_func=products_view.get_products, methods=['GET'])
my_v1.add_url_rule('/update_product', view_func=products_view.update_product, methods=['PATCH'])
my_v1.add_url_rule('/delete_product/<int:product_id>', view_func=products_view.deleteproduct, methods=['DELETE'])
my_v1.add_url_rule('/product_detail/<int:product_id>', view_func=products_view.productdetail, methods=['GET'])
my_v1.add_url_rule('/checked_soldout/<int:product_id>', view_func=products_view.checked_soldout, methods=['PATCH'])
my_v1.add_url_rule('/create_service', view_func=service.createservice, methods=['POST'])
