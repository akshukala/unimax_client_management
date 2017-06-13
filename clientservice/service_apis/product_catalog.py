from uni_db.client_erp.models import Product, ProductCategory
from django.core.exceptions import ObjectDoesNotExist

from flask.globals import request
from clientservice.utils.resource import Resource


class ProductCatalog(Resource):

    def get(self):
        try:
            return [{"name": category.name,
                     "id": category.id,
                     "product_count": Product.objects.filter(category=category,
                                                             active=True).count() 
                     }for category in ProductCategory.objects.all()]
        except ObjectDoesNotExist:
            return
            {
             'errorCode': 400,
             'errorMessage': "Category not found"
            }

class ProductByCategories(Resource):
    def get(self):
        category_id = request.args.get('category_id')
        try:
            return [{"name": product.product_name,
                     "category": product.category.name,
                     "mrp": product.mrp,
                     "sellingPrice": product.selling_price,
                     "weight": product.weight,
                     "gst": product.gst,
                     "item_sku": product.id
                     }
                    for product in
                    Product.objects.filter(category=ProductCategory.objects.get(id=int(category_id)),active=True)]
        except ObjectDoesNotExist:
            return
            {
             'errorCode': 400,
             'errorMessage': "Product not found"
            }