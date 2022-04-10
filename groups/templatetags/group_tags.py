from django import template
from ..models import Group,GroupMember

register = template.Library()

@register.inclusion_tag('clonemedia\posts\templates\posts\post_list.html')
def get_other_group():
    group_members = GroupMember.objects.all()
    other_groups = Group.objects.all()
    return {'other_group':other_groups, 'group_member':group_members }

