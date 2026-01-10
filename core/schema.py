from graphene import ObjectType, Schema
import products.schema
import graphql_jwt


class Query(products.schema.Query, ObjectType):
    pass


class Mutation(products.schema.Mutation, ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = Schema(query=Query, mutation=Mutation)
