from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.String()
    title = fields.String(min_length=1, max_length=255, required=True)
    description = fields.String(max_length=4096)
    subcategories = fields.List(fields.String, dump_only=True)
    parent = fields.String()
    is_root = fields.Bool(default=False)


class ProductSchema(Schema):
    id = fields.String()
    title = fields.String(min_length=1, max_length=255, required=True)
    img_url = fields.String(max_length=1024)
    category = fields.String(required=True)
    article = fields.String(max_length=64, required=True)
    description = fields.String(max_length=4096)
    price = fields.Int(min_value=1, required=True)
    in_stock = fields.Int(min_value=0, default=0)
    discount_price = fields.Int(min_value=1, required=False)


class UserSchema(Schema):
    id = fields.String()
    telegram_id = fields.String(max_length=32, required=True, unique=True)
    username = fields.String(max_length=128)
    creation_date = fields.DateTime()
    total = fields.Int(min_value=0)
