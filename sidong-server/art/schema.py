from django.db import transaction
from graphene import ObjectType, Field, List, ID, Mutation, String, \
    Int, Boolean, Argument, InputObjectType, InputField
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
from django.contrib.auth.models import User
from art.models import Theme, Style, Technique, Art, \
    calculate_art_size, Like, calculate_orientation
from file.models import File, create_file, validate_file
from user.models import Artist
from django.utils import timezone


class ArtImageType(ObjectType):
    id = ID()
    url = String()


class ArtType(DjangoObjectType):
    class Meta:
        model = Art
        convert_choices_to_enum = ["size"]

    representative_image_url = String()
    image_urls = List(ArtImageType)
    current_user_likes_this = Boolean()

    def resolve_representative_image_url(self, info):
        return self.representative_image_url

    def resolve_image_urls(self, info):
        image_urls = []
        for image_id in self.images:
            file_instance = File.objects.get(id=image_id)
            image_urls.append({
                'id': image_id,
                'url': file_instance.url,
            })

        return image_urls

    def resolve_current_user_likes_this(self, info):
        user = info.context.user
        if user.is_anonymous:
            return False
        return Like.objects.filter(user=user, art_id=self.id).exists()

    def resolve_created_at(self, info):
        return timezone.localdate(self.created_at)


class ThemeType(DjangoObjectType):
    class Meta:
        model = Theme
        convert_choices_to_enum = False


class StyleType(DjangoObjectType):
    class Meta:
        model = Style
        convert_choices_to_enum = False


class TechniqueType(DjangoObjectType):
    class Meta:
        model = Technique
        convert_choices_to_enum = False


class ArtOptions(ObjectType):
    themes = List(ThemeType)
    styles = List(StyleType)
    techniques = List(TechniqueType)


class ArtLikeType(ObjectType):
    id = ID()
    last_like_id = ID()
    arts = List(ArtType)


class CursorBasedArts(ObjectType):
    last_id = ID()
    arts = List(ArtType)


class ArtConnection(ObjectType):
    arts = List(ArtType)
    total_count = Int()


class SaleStatusInput(InputObjectType):
    all = InputField(Boolean)
    on_sale = InputField(Boolean)
    sold_out = InputField(Boolean)
    not_for_sale = InputField(Boolean)


class OrientationInput(InputObjectType):
    all = InputField(Boolean)
    landscape = InputField(Boolean)
    portrait = InputField(Boolean)
    square = InputField(Boolean)
    etc = InputField(Boolean)


class ArtSizeInput(InputObjectType):
    all = InputField(Boolean)
    small = InputField(Boolean)
    medium = InputField(Boolean)
    large = InputField(Boolean)


class Query(ObjectType):
    art = Field(ArtType, art_id=ID())
    art_options = Field(ArtOptions, medium_id=ID())
    arts = List(ArtType, page=Int(),
                page_size=Int(), sale_status=Argument(SaleStatusInput),
                orientation=Argument(OrientationInput), size=Argument(ArtSizeInput),
                price=List(Int), medium=String(), style=String(),
                technique=String(), theme=String(), ordering_priority=List(String))
    arts_by_artist = List(ArtType, artist_id=ID(), last_art_id=ID())
    current_user_arts_offset_based = Field(
        ArtConnection, page=Int(), page_size=Int())
    user_liking_arts = Field(ArtLikeType, user_id=ID(required=True),
                             last_like_id=ID())
    search_arts = Field(CursorBasedArts, last_id=ID(),
                        word=String(required=True))

    def resolve_art(self, info, art_id):
        return Art.objects.get(id=art_id)

    def resolve_art_options(self, info, medium_id=None):
        if medium_id is None:
            return None

        themes = Theme.objects.filter(medium=medium_id).order_by('name')
        styles = Style.objects.filter(medium=medium_id).order_by('name')
        techniques = Technique.objects.filter(
            medium=medium_id).order_by('name')

        return ArtOptions(
            themes=themes,
            styles=styles,
            techniques=techniques,
        )

    def resolve_arts(self, info, page=0, page_size=20,
                     sale_status=None, size=None, orientation=None, price=None,
                     medium=None, theme=None, style=None, technique=None,
                     ordering_priority=None):

        arts_filter = {}

        if sale_status:     # 필터 적용
            sale_status_list = []
            orientation_list = []
            size_list = []

            if sale_status['all'] is False:
                if sale_status['on_sale'] is True:
                    sale_status_list.append(Art.ON_SALE)
                if sale_status['sold_out'] is True:
                    sale_status_list.append(Art.SOLD_OUT)
                if sale_status['not_for_sale'] is True:
                    sale_status_list.append(Art.NOT_FOR_SALE)
                arts_filter['sale_status__in'] = sale_status_list

            if orientation['all'] is False:
                if orientation['landscape'] is True:
                    orientation_list.append(Art.LANDSCAPE)
                if orientation['portrait'] is True:
                    orientation_list.append(Art.PORTRAIT)
                if orientation['square'] is True:
                    orientation_list.append(Art.SQUARE)
                if orientation['etc'] is True:
                    orientation_list.append(Art.ETC_ORIENTATION)
                arts_filter['orientation__in'] = orientation_list

            if size['all'] is False:
                if size['small'] is True:
                    size_list.append(Art.SMALL)
                if size['medium'] is True:
                    size_list.append(Art.MEDIUM)
                if size['large'] is True:
                    size_list.append(Art.LARGE)
                arts_filter['size__in'] = size_list

            if medium != 'all':
                arts_filter['medium'] = medium
            if style != 'all':
                arts_filter['style'] = style
            if technique != 'all':
                arts_filter['technique'] = technique
            if theme != 'all':
                arts_filter['theme'] = theme

            arts_filter['price__range'] = price

        arts = Art.objects.filter(**arts_filter)

        if not arts:
            return None

        if ordering_priority is None:
            ordering_priority = ['-id']

        return arts.order_by(*ordering_priority)[page*page_size:(page + 1)*page_size]

    def resolve_arts_by_artist(self, info, artist_id, last_art_id=None):
        arts = Art.objects.filter(artist_id=artist_id)

        if not arts:
            return None

        arts_filter = {}
        if last_art_id:
            arts_filter = {'id__lt': last_art_id}

        return arts.filter(**arts_filter).order_by('-id')[:20]

    def resolve_current_user_arts_offset_based(self, info, page=0, page_size=10):
        user = info.context.user
        if user.is_anonymous:
            return None

        arts = Art.objects.filter(artist__user=user)

        return {
            'arts': arts.order_by('-id')[page*page_size:(page + 1)*page_size],
            'total_count': arts.count(),
        }

    def resolve_user_liking_arts(self, info, user_id, last_like_id=None):
        like_instances = Like.objects.filter(
            user=User.objects.get(id=user_id))

        if not like_instances:
            return None

        like_filter = {'id__lt': last_like_id} if last_like_id else {}

        like_instances = like_instances.filter(
            **like_filter).order_by('-id')[:20]

        return {
            'id': user_id,
            'last_like_id': like_instances[len(like_instances) - 1].id if like_instances else None,
            'arts': [like.art for like in like_instances],
        }

    def resolve_search_arts(self, info, word, last_id=None):
        if not word:
            return None

        arts = Art.objects.filter(name__icontains=word)
        if not arts:
            return None

        arts_filter = {'id__lt': last_id} if last_id else {}

        arts = arts.filter(**arts_filter).order_by('-id')[:20]

        return {
            'last_id': arts[len(arts) - 1].id if arts else None,
            'arts': arts,
        }


class CreateArt(Mutation):
    class Arguments:
        art_images = Upload(required=True)
        description = String(required=True)
        width = Int(required=True)
        height = Int(required=True)
        is_framed = Boolean(required=True)
        medium = ID(required=True)
        name = String(required=True)
        price = Int()
        delivery_fee = Int()
        sale_status = ID(required=True)
        style = ID(required=True)
        technique = ID(required=True)
        theme = ID(required=True)

    success = Boolean()
    msg = String()

    @transaction.atomic
    def mutate(self, info, art_images, description, width,
               height, is_framed, medium, name,
               sale_status, style, technique, theme, price=None, delivery_fee=None):
        current_user = info.context.user

        for image in art_images:
            validate_image = validate_file(image, File.BUCKET_ASSETS)
            if validate_image['status'] == 'fail':
                return CreateArt(success=False, msg=validate_image['msg'])

        image_file_ids = []

        for image in art_images:
            image_file = create_file(image, File.BUCKET_ASSETS, current_user)
            if image_file['status'] == 'fail':
                return CreateArt(success=False, msg=image_file['msg'])
            image_file_ids.append(image_file['instance'].id)

        Art.objects.create(
            artist=current_user.artist,
            images=image_file_ids,
            description=description,
            width=width,
            height=height,
            size=calculate_art_size(width, height),
            is_framed=is_framed,
            medium=medium,
            name=name,
            orientation=calculate_orientation(width, height),
            price=price if price else 0,
            delivery_fee=delivery_fee if delivery_fee else 0,
            sale_status=sale_status,
            style=Style.objects.get(id=style),
            technique=Technique.objects.get(id=technique),
            theme=Theme.objects.get(id=theme),
        )

        return CreateArt(success=True)


class UpdateArt(Mutation):
    class Arguments:
        art_id = ID(required=True)
        art_images = List(ID, required=True)
        description = String(required=True)
        width = Int(required=True)
        height = Int(required=True)
        is_framed = Boolean(required=True)
        medium = ID(required=True)
        name = String(required=True)
        price = Int()
        delivery_fee = Int()
        sale_status = ID(required=True)
        style = ID(required=True)
        technique = ID(required=True)
        theme = ID(required=True)

    success = Boolean()
    msg = String()

    def mutate(self, info, art_id, art_images, description, width,
               height, is_framed, medium, name,
               sale_status, style, technique, theme, price=None, delivery_fee=None):

        art = Art.objects.filter(id=art_id)

        if info.context.user.id != art.get().artist.user.id:
            return UpdateArt(success=False, msg="작품을 수정할 권한이 없습니다.")

        art.update(
            images=art_images,
            description=description,
            width=width,
            height=height,
            size=calculate_art_size(width, height),
            is_framed=is_framed,
            medium=medium,
            name=name,
            orientation=calculate_orientation(width, height),
            price=price if price else 0,
            delivery_fee=delivery_fee if delivery_fee else 0,
            sale_status=sale_status,
            style=Style.objects.get(id=style),
            technique=Technique.objects.get(id=technique),
            theme=Theme.objects.get(id=theme),
        )

        return UpdateArt(success=True)


class DeleteArt(Mutation):
    class Arguments:
        art_id = ID(required=True)

    success = Boolean()
    msg = String()

    def mutate(self, info, art_id):
        art = Art.objects.filter(id=art_id)

        if info.context.user.id != art.get().artist.user.id:
            return DeleteArt(success=False, msg="작품을 삭제할 권한이 없습니다.")

        art.delete()
        return DeleteArt(success=True)


class LikeArt(Mutation):
    class Arguments:
        art_id = ID(required=True)

    success = Boolean()

    def mutate(self, info, art_id):
        user = info.context.user
        if user.is_anonymous:
            return LikeArt(success=False)

        art = Art.objects.get(id=art_id)
        Like.objects.create(user=user, art=art)
        art.like_count += 1
        art.save()

        return LikeArt(success=True)


class CancelLikeArt(Mutation):
    class Arguments:
        art_id = ID(required=True)

    success = Boolean()

    def mutate(self, info, art_id):
        user = info.context.user
        if user.is_anonymous:
            return CancelLikeArt(success=False)

        art = Art.objects.get(id=art_id)
        like = Like.objects.filter(user=user, art=art)
        like.delete()

        if art.like_count > 0:
            art.like_count -= 1
            art.save()

        return CancelLikeArt(success=True)


class Mutation(ObjectType):
    create_art = CreateArt.Field()
    update_art = UpdateArt.Field()
    delete_art = DeleteArt.Field()
    like_art = LikeArt.Field()
    cancel_like_art = CancelLikeArt.Field()
