
import graphene
from .models import User, Contact, ContactData
from django.db import transaction
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = ('name',)
    user_id = graphene.ID(required=True)


class AddUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    
    Output = UserType
    @classmethod
    def mutate(cls, root, info, name):
        with transaction.atomic():
            user = User.objects.create(name=name)
            return UserType(
                user_id=user.id,
                name=user.name
            )


class RemoveUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    @classmethod
    def mutate(cls, root, info, user_id):
        with transaction.atomic():
            User.objects.get(id=user_id).delete()


class ContactDataType(DjangoObjectType):
    class Meta:
        model = ContactData
        fields = ('type', 'value')


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact
        fields = ('user_id', 'name', 'contact_data')
    contact_id = graphene.ID(required=True)
    contact_data = graphene.List(graphene.NonNull(ContactDataType))


class AddContactsDataInput(graphene.InputObjectType):
    type = graphene.String(required=True)
    value = graphene.String(required=True)


class AddContactsInput(graphene.InputObjectType):
    user_id = graphene.String(required=True)
    name = graphene.String(required=True)
    contact_data = graphene.List(graphene.NonNull(AddContactsDataInput))


class AddContacts(graphene.Mutation):
    class Arguments:
        input = AddContactsInput(required=True)

    Output = ContactType

    @classmethod
    def mutate(cls, root, info, input):
        with transaction.atomic():
            contact = Contact.objects.create(
                user_id=input.user_id, 
                name=input.name,
            )
            contact_data = ContactData.objects.bulk_create(
                ContactData(
                    contact=contact,
                    type=cd.type,
                    value=cd.value
                )
                for cd in input.contact_data
            )
            return ContactType(
                contact_id = contact.id,
                user_id = contact.user.id,
                name = contact.name,
                contact_data = contact_data
            )


class RemoveContact(graphene.Mutation):
    class Arguments:
        contact_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    @classmethod
    def mutate(cls, root, info, contact_id):
        with transaction.atomic():
            Contact.objects.get(id=contact_id).delete()


class Query(graphene.ObjectType):
    get_contact = graphene.Field(ContactType, contact_id=graphene.ID())
    

    def resolve_get_contact(root, info, contact_id):
        return Contact.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    add_user = AddUser.Field()
    remove_user = RemoveUser.Field()
    add_contact = AddContacts.Field()
    remove_contact = RemoveContact.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)