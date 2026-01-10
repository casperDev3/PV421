from graphene import List, Field, Int, ObjectType, Mutation, String, Decimal, ID, Boolean
from graphene_django import DjangoObjectType
from .models import Product
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required


# TYPES
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "user", "is_available"]


# MUTATIONS
class CreateProductMutation(Mutation):
    product = Field(ProductType)

    class Arguments:
        name = String(required=True)
        price = Decimal(required=True)
        description = String()

    def mutate(self, info, name, price, description=None):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Ви повинні увійти в систему, щоб додавати продукти!")

        new_product = Product(
            name=name,
            price=price,
            description=description,
            user=user
        )

        new_product.save()
        return CreateProductMutation(product=new_product)


class UpdateProductMutation(Mutation):
    class Arguments:
        id = ID(required=True)
        name = String()
        description = String()
        price = Decimal()
        is_available = Boolean()

    product = Field(ProductType)
    ok = Boolean()

    @login_required
    def mutate(self, info, id, name=None, description=None, price=None, is_available=None):
        user = info.context.user
        try:
            product_instance = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return UpdateProductMutation(ok=False, product=None)
        # if product_instance.user != user:
        #     raise Exception("Ви не маєте дозволу оновлювати цей продукт!")

        if name is not None:
            product_instance.name = name
        if description is not None:
            product_instance.description = description
        if price is not None:
            product_instance.price = price
        if is_available is not None:
            product_instance.is_available = is_available

        product_instance.save()
        return UpdateProductMutation(ok=True, product=product_instance)


class DeleteProductMutation(Mutation):
    class Arguments:
        id = ID(required=True)

    ok = Boolean()

    def mutate(self, info, id):
        try:
            product_instance = Product.objects.get(pk=id)
            product_instance.delete()
            return DeleteProductMutation(ok=True)
        except Product.DoesNotExist:
            return DeleteProductMutation(ok=False)


class Mutation(ObjectType):
    create_product = CreateProductMutation.Field()
    update_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()


# QUERY
class Query(ObjectType):
    all_products = List(ProductType)
    product_by_id = Field(ProductType, id=Int(required=True))

    def resolve_all_products(self, info):
        return Product.objects.select_related('user').all()

    def resolve_product_by_id(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None
