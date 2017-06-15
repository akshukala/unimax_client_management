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

    def post(self):
        request_data = request.get_json(force=True)
        try:
            Product.objects.get_or_create(product_name = str(request_data['p_name']),
                        product_code = str(request_data['p_code']),
                        category = ProductCategory.objects.get(id=int(request_data['p_category'])),
                        mrp = float(request_data['p_mrp']),
                        selling_price = float(request_data['p_sellingprice']),
                        weight = float(request_data['p_weight']),
                        gst = str(request_data['p_gst']),
                        description = str(request_data['p_desc']))

            return {"responseCode":"200",
                    "Message":"Product Successfully Added"}
        except:
            return {"responseCode":"400",
                    "Message":"Something went wrong"}
        

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
        