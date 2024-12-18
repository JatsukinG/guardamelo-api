from graphene import relay, Field, String, ID, Boolean, List, Node
from graphql import GraphQLError
from graphql_relay import from_global_id

from accounts.models import User
from projects.choices import NOTE_VISIBILITY_CHOICES
from projects.models import Project, Note
from projects.nodes import ProjectNode, NoteNode


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


class CreateNote(relay.ClientIDMutation):
    note = Field(NoteNode)

    class Input:
        project_id = ID(required=True)
        title = String(required=True)
        content = String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, project_id, **input):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to create a note.")

        _, decoded_project_id = from_global_id(project_id)

        try:
            project = Project.objects.get(id=decoded_project_id, user=user)
        except Project.DoesNotExist:
            raise GraphQLError("Project not found or you do not have permission")

        note = Note(
            project=project,
            **input
        )
        note.save()

        return CreateNote(note=note)


class UpdateNote(relay.ClientIDMutation):
    note = Field(NoteNode)

    class Input:
        id = ID(required=True)
        title = String(required=False)
        content = String(required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, **input):
        user = info.context.user
        _, decoded_id = from_global_id(id)

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to update a note.")

        try:
            note = Note.objects.get(id=decoded_id, project__user=user)
        except Note.DoesNotExist:
            raise GraphQLError("Note not found or you do not have permission")

        for field, value in input.items():
            setattr(note, field, value)

        note.save()
        return UpdateNote(note=note)


class DeleteNote(relay.ClientIDMutation):
    success = Boolean()

    class Input:
        id = ID(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        user = info.context.user
        _, decoded_id = from_global_id(id)

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to delete a note.")

        try:
            note = Note.objects.get(id=decoded_id, project__user=user)
        except Note.DoesNotExist:
            raise GraphQLError("Note not found or you do not have permission")

        note.delete()
        return DeleteNote(success=True)


class UpdateNoteVisibility(relay.ClientIDMutation):
    success = Boolean()

    class Input:
        id = ID(required=True)
        visibility = String(required=True)
        shared_with = List(ID, required=False)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, visibility, shared_with=None):
        user = info.context.user
        print(user, id, visibility)
        note = Node.get_node_from_global_id(info, id, only_type=NoteNode)

        if user.is_anonymous:
            raise GraphQLError("You must be logged in to delete a note.")

        if note.project.user != user:
            raise GraphQLError("You do not have permission to change this note's visibility.")

        if visibility not in [choice[0] for choice in NOTE_VISIBILITY_CHOICES]:
            raise GraphQLError("Invalid visibility option.")

        note.visibility = visibility

        if visibility == 'shared' and shared_with:
            users = User.objects.filter(id__in=shared_with)
            note.shared_with.set(users)
        else:
            note.shared_with.clear()

        note.save()
        return UpdateNoteVisibility(success=True)
