# REST API for the chat models are defined here
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS

from tastypie.resources import ModelResource
from chat.models import Chat, Metadata, MetadataName, Ticket, Tag
from core.api.resources import ProjectResource, UserResource


class TagResource(ModelResource):

    class Meta:
        resource_name = 'tag'
        queryset = Tag.objects.all()
        allowed_methods = ['get', 'delete', 'put', 'post']
        authorization = Authorization()


class TicketResource(ModelResource):

    user = fields.ForeignKey(UserResource, 'assignee', full=True, null=True)
    tag = fields.ManyToManyField(TagResource, 'tag', full=True, null=True)

    class Meta:
        resource_name = 'ticket'
        queryset = Ticket.objects.all()
        allowed_methods = ['get', 'delete', 'put', 'post']
        authorization = Authorization()
        filtering = {
            'id': ALL_WITH_RELATIONS,
        }


class ChatResource(ModelResource):

    project = fields.ForeignKey(ProjectResource, 'project')

    class Meta:
        resource_name = 'chat'
        queryset = Chat.objects.all()
        allowed_methods = ['get']
        filtering = {
            'project': ALL_WITH_RELATIONS,
            'id': ALL_WITH_RELATIONS,
        }


class MetadataNameResource(ModelResource):

    class Meta:
        resource_name = 'metadata_name'
        queryset = MetadataName.objects.all()
        allowed_methods = ['get', 'delete', 'put', 'post']
        authorization = Authorization()


class MetadataResource(ModelResource):

    metadata_name = fields.ForeignKey(MetadataNameResource, 'metadata_name', full=True)
    chat = fields.ForeignKey(ChatResource, 'chat', full=True)

    class Meta:
        resource_name = 'metadata'
        queryset = Metadata.objects.all()
        allowed_methods = ['get', 'delete', 'put', 'post']
        authorization = Authorization()
        filtering = {
            'chat': ALL_WITH_RELATIONS,
            'metadata_name': ALL_WITH_RELATIONS,
        }