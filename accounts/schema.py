import graphene
from graphql_jwt import ObtainJSONWebToken, Verify, Refresh
from graphene import ObjectType, Field

from accounts.mutations import CreateUser, UpdateMe, ChangePassword
from accounts.nodes import UserNode


class Query(ObjectType):
    me = Field(UserNode)

    def resolve_me(self, info):
        return info.context.user


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()

    create_user = CreateUser.Field()
    update_user = UpdateMe.Field()
    change_password = ChangePassword.Field()
