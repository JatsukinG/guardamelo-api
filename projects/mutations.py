from graphene import relay, Field, String, ID, Boolean
from graphql import GraphQLError
from graphql_relay import from_global_id

from projects.models import Project, Document
from projects.nodes import ProjectNode, DocumentNode


class CreateProject(relay.ClientIDMutation):
    project = Field(ProjectNode)

    class Input:
        name = String(required=True)
        description = String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to create a project.")

        project = Project(user=user, **input)
        project.save()

        return CreateProject(project=project)


class UpdateProject(relay.ClientIDMutation):
    project = Field(ProjectNode)

    class Input:
        id = ID(required=True)
        name = String(required=True)
        description = String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, **input):
        user = info.context.user
        _, decoded_id = from_global_id(id)

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to update a project.")

        try:
            project = Project.objects.get(id=decoded_id, user=user)
        except Project.DoesNotExist:
            raise GraphQLError("Project not found or you do not have permission")

        for field, value in input.items():
            setattr(project, field, value)

        project.save()
        return UpdateProject(project=project)


class DeleteProject(relay.ClientIDMutation):
    success = Boolean()

    class Input:
        id = ID(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        user = info.context.user
        _, decoded_id = from_global_id(id)

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to delete a project.")

        try:
            project = Project.objects.get(id=decoded_id, user=user)
        except Project.DoesNotExist:
            raise GraphQLError("Project not found or you do not have permission")

        project.delete()
        return DeleteProject(success=True)


class CreateDocument(relay.ClientIDMutation):
    document = Field(DocumentNode)

    class Input:
        project_id = ID(required=True)
        title = String(required=True)
        content = String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, project_id, **input):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to create a document.")

        _, decoded_project_id = from_global_id(project_id)

        try:
            project = Project.objects.get(id=decoded_project_id, user=user)
        except Project.DoesNotExist:
            raise GraphQLError("Project not found or you do not have permission")

        document = Document(
            project=project,
            **input
        )
        document.save()

        return CreateDocument(document=document)


class UpdateDocument(relay.ClientIDMutation):
    document = Field(DocumentNode)

    class Input:
        id = ID(required=True)
        title = String(required=False)
        content = String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, **input):
        user = info.context.user
        _, decoded_id = from_global_id(id)

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to update a document.")

        try:
            document = Document.objects.get(id=decoded_id, project__user=user)
        except Document.DoesNotExist:
            raise GraphQLError("Document not found or you do not have permission")

        for field, value in input.items():
            setattr(document, field, value)

        document.save()
        return UpdateDocument(document=document)


class DeleteDocument(relay.ClientIDMutation):
    success = Boolean()

    class Input:
        id = ID(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        user = info.context.user
        _, decoded_id = from_global_id(id)

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to delete a document.")

        try:
            document = Document.objects.get(id=decoded_id, project__user=user)
        except Document.DoesNotExist:
            raise GraphQLError("Document not found or you do not have permission")

        document.delete()
        return DeleteDocument(success=True)
