from graphene import ObjectType, Schema
import products.schema


class Query(products.schema.Query, ObjectType):
    pass


class Mutation(products.schema.Mutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
