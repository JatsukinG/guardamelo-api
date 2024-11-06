from graphene import relay, Field, String
from graphql import GraphQLError
from graphql_relay import from_global_id

from projects.models import Project
from projects.nodes import ProjectNode


class ProjectFieldBase:
    name = String(required=True)
    description = String(required=False)


class CreateProject(relay.ClientIDMutation):
    project = Field(ProjectNode)

    class Input(ProjectFieldBase):
        pass

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user

        project = Project()

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to create a project.")

        for field, value in input.items():
            if hasattr(value, "value"):
                value = value.value

            setattr(project, field, value)

        project.user = user
        project.save()

        return CreateProject(project=project)


class UpdateProject(relay.ClientIDMutation):
    project = Field(ProjectNode)

    class Input(ProjectFieldBase):
        id = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, **input):
        user = info.context.user
        _, decoded_id = from_global_id(id)

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to update a project.")

        try:
            project = Project.objects.get(id=decoded_id)
        except Project.DoesNotExist:
            raise GraphQLError("Project not found")

        for field, value in input.items():
            if hasattr(value, "value"):
                value = value.value

            setattr(project, field, value)

        project.save()

        return UpdateProject(project=project)
