from graphene import ObjectType, Schema
import products.schema


class Query(products.schema.Query, ObjectType):
    pass


schema = Schema(query=Query)
