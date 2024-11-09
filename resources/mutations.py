from graphene import relay, Field, String, ID, Boolean, JSONString
from graphql import GraphQLError
from graphql_relay import from_global_id

from resources.models import Resource
from resources.nodes import ResourceNode


class CreateResource(relay.ClientIDMutation):
    resource = Field(ResourceNode)

    class Input:
        title = String(required=True)
        content = String(required=True)
        description = String(required=False)
        image = String(required=False)
        tags = JSONString(required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to create a resource.")

        resource = Resource(author=user, **input)
        resource.save()

        return CreateResource(resource=resource)


class UpdateResource(relay.ClientIDMutation):
    resource = Field(ResourceNode)

    class Input:
        id = ID(required=True)
        title = String(required=False)
        content = String(required=False)
        description = String(required=False)
        image = String(required=False)
        tags = JSONString(required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, **input):
        user = info.context.user
        _, decoded_id = from_global_id(id)

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to update a resource.")

        try:
            resource = Resource.objects.get(id=decoded_id, author=user)
        except Resource.DoesNotExist:
            raise GraphQLError("Resource not found or you do not have permission")

        for field, value in input.items():
            setattr(resource, field, value)

        resource.save()
        return UpdateResource(resource=resource)


class DeleteResource(relay.ClientIDMutation):
    success = Boolean()

    class Input:
        id = ID(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        user = info.context.user
        _, decoded_id = from_global_id(id)

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to delete a resource.")

        try:
            resource = Resource.objects.get(id=decoded_id, author=user)
        except Resource.DoesNotExist:
            raise GraphQLError("Resource not found or you do not have permission")

        resource.delete()
        return DeleteResource(success=True)
