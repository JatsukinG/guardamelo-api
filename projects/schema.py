from graphene import ObjectType, relay, String
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_relay import from_global_id

from projects.models import Note
from projects.mutations import CreateProject, UpdateProject, DeleteProject, CreateNote, UpdateNote, \
    DeleteNote, UpdateNoteVisibility
from projects.nodes import ProjectNode, NoteNode


class Query(ObjectType):
    project = relay.Node.Field(ProjectNode)
    projects = DjangoFilterConnectionField(ProjectNode)

    note = relay.Node.Field(NoteNode)
    notes = DjangoFilterConnectionField(
        NoteNode,
        project_id=String(required=True)
    )

    def resolve_notes(root, info, project_id: str, **kwargs):
        _, project_id = from_global_id(project_id)
        if project_id is not '':
            return Note.objects.filter(project__id=project_id)
        else:
            raise GraphQLError('Please enter a valid project_id')


class Mutation(ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()

    create_note = CreateNote.Field()
    update_note = UpdateNote.Field()
    delete_note = DeleteNote.Field()
    update_note_visibility = UpdateNoteVisibility.Field()
