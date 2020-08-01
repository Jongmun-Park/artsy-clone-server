from art.models import Category, Art
from graphene import Field, Int, String, List, Mutation
from graphene_django.types import DjangoObjectType


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class ArtType(DjangoObjectType):
    class Meta:
        model = Art


class CreateArt(Mutation):
    class Arguments:
        name = String(required=True)
        # file =


class Query(object):
    category = Field(CategoryType, id=Int(), name=String())
    all_categories = List(CategoryType)

    art = Field(ArtType, id=Int(), name=String())
    all_arts = List(ArtType)

    def resolve_category(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return Category.objects.get(id=id)

        if name is not None:
            return Category.objects.get(name=name)

        return None

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_art(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id is not None:
            return Art.objects.get(id=id)

        if name is not None:
            return Art.objects.get(name=name)

        return None

    def resolve_all_arts(self, info, **kwargs):
        return Art.objects.select_related("category").all()
