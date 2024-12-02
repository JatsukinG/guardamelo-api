from projects.enums.note_visibility import NoteVisibility

NOTE_VISIBILITY_CHOICES = (
    (NoteVisibility.PUBLIC.value, "Pública"),
    (NoteVisibility.PRIVATE.value, "Privada"),
    (NoteVisibility.SHARED.value, "Compartida"),
)
