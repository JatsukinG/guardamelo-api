from django.contrib.auth import get_user_model
from graphene import relay, Field, String
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from accounts.nodes import UserNode


class UserInput:
    first_name = String(required=True)
    last_name = String(required=True)
    phone = String(required=False)
    email = String(required=True)


class CreateUser(relay.ClientIDMutation):
    user = Field(UserNode)

    class Input(UserInput):
        password = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        user = get_user_model()

        first_name = input.get('first_name')
        last_name = input.get('last_name')
        email = input.get('email')
        phone = input.get('phone')

        try:
            user = user.objects.get(email=email)
            raise GraphQLError("Ya existe un usuario con este correo electrónico.")
        except user.DoesNotExist:
            pass

        print("Creating user...")
        user = user.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        user.set_password(input.get('password'))
        user.save()

        return CreateUser(user=user)


class UpdateMe(relay.ClientIDMutation):
    user = Field(UserNode)

    class Input(UserInput):
        pass

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user
        email = input.get('email')

        if email and email != user.email:
            try:
                user = get_user_model().objects.get(email=email)
                raise GraphQLError("Ya existe un usuario con este correo electrónico.")
            except user.DoesNotExist:
                pass

        for field, value in input.items():
            if hasattr(user, field):
                setattr(user, field, value)

        user.save()

        return UpdateMe(user=user)


class ChangePassword(relay.ClientIDMutation):
    user = Field(UserNode)

    class Input:
        current_password = String(required=True)
        new_password = String(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user

        if not user.check_password(input.get('current_password')):
            raise GraphQLError("Contraseña actual incorrecta.")

        user.set_password(input.get('new_password'))
        user.save()

        return ChangePassword(user=user)
