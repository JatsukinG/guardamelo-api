import graphene

import accounts.schema
import projects.schema


class Query(
    accounts.schema.Query,
    projects.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    accounts.schema.Mutation,
    projects.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
