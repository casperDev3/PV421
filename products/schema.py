from graphene import List, Field, Int, ObjectType
from graphene_django import DjangoObjectType
from .models import Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "user", "is_available" ]


class Query(ObjectType):
    all_products = List(ProductType)
    product_by_id = Field(ProductType, id=Int(required=True))

    def resolve_all_products(self, info):
        return Product.objects.all()

    def resolve_product_by_id(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None
