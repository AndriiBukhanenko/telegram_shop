from flask import request
from flask_restful import Resource
from mongoengine import DoesNotExist

from api.schema import CategorySchema, ProductSchema, UserSchema
from models.model import Category, Product, User


class CategoryResource(Resource):
    """
    Category Resource to CRUD data for Categories
    """

    def get(self, cat_id=None):
        """GET method for categories
            :param cat_id ID of category. If absent - returns all the existing categories
        """
        many = not cat_id
        try:
            query = Category.objects.get(id=cat_id) if cat_id else Category.objects()
        except DoesNotExist:
            return {'msg': f'Category with id {cat_id} not exists'}
        return CategorySchema().dump(query, many=many)

    def post(self):
        """POST method for categories


        """
        err = CategorySchema().validate(request.json)

        if err:
            return err

        cat = Category(**request.json).save()
        return CategorySchema().dump(cat)

    def put(self, cat_id):
        """ PUT method for updating
            Takes the json like
            {
                "title": "Updated category name",
            }
        :param cat_id: category id that we want to update
        """
        if not cat_id:
            return {'msg': 'cat_id not defined for update'}
        cat = Category.objects.get(id=cat_id)
        cat.modify(**request.json)
        return CategorySchema().dump(cat)

    def delete(self, cat_id):
        """ DELETE method for remove category
       :param cat_id: category id that we want to delete
       """
        if not cat_id:
            return {'msg': 'cat_id not defined for update'}
        Category.objects.get(id=cat_id).delete()
        return {'msg': 'deleted'}


class ProductResource(Resource):
    def get(self, product_id=None):
        """GET method for select product
        :param product_id: product id that we want to select. If absent - seects all the products
        """
        many = not product_id
        try:
            query = Product.objects.get(id=product_id) if product_id else Product.objects()
        except DoesNotExist:
            return {'msg': f'Product with id {product_id} not exists'}
        return ProductSchema().dump(query, many=many)

    def post(self):
        """POST method for Product
        :param
        Takes json with fields like
            {
                "title": "Panasonic KX-TGE434B",
                "article": "KX-TGE434B",
                "description": "Expandable Cordless Phone System with Answering Machine - 4 Handsets - KX-TGE434B",
                "in_stock": 100,
                "id": "5e56d68c91e9935029e6b986",
                "price": 10995,
                "category": "Panasonic",
                "discount_price": 10000,
                "img_url": "https://shop.panasonic.com/dw/image/v2/AASQ_PRD/on/demandware.static/-/Sites-shop-pna-master-catalog/default/dw28e2f194/product/images/KX-TGE434B_ALT01.jpg?sw=1000&sh=1000&sm=fit"
            }
        :return: The json with new project inserted
        """
        err = ProductSchema().validate(request.json)
        if err:
            return err
        product = Product(**request.json).save()
        return ProductSchema().dump(product)

    def put(self, product_id):
        """ PUT method for updating product
            Takes the json like
            {
                "title": "Updated product name",
                "price": [Updated price like 15000]
            }
        :param product_id: product id that we want to update
        """
        if not product_id:
            return {'msg': 'cat_id not defined for update'}
        product = Product.objects.get(id=product_id)
        product.modify(**request.json)
        return ProductSchema().dump(product)

    def delete(self, product_id):
        """ DELETE method for remove product
        :param product_id: product id that we want to delete
        """
        if not product_id:
            return {'msg': 'cat_id not defined for update'}
        Product.objects.get(id=product_id).delete()
        return {'msg': 'deleted'}


class UserResource(Resource):
    def get(self, user_id=None):
        """ GET method for showing User information

        :return: json with User information
        """
        many = not user_id
        try:
            query = User.objects.get(id=user_id) if user_id else User.objects()
        except DoesNotExist:
            return {'msg': f'User with id {user_id} not exists'}

        if user_id:
            query.calc_total()
        else:
            users = [user for user in query]
            for user in users:
                user.calc_total()
        return UserSchema().dump(query, many=many)
