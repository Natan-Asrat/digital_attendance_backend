from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProgramViewset, 
    ProgramInviteViewset, 
    ProgramInvitedOrganizationViewset, 
    NestedOrganizationProgramViewset,
    NestedProgramInviteViewset,
    NestedOrganizationAssociatedProgramViewset,
    NestedOrganizationInviteViewset,
    NestedSubscribersViewset,
    NestedSubscribedProgramsViewset
)
from account.views import UserSimpleViewset
from organization.views import OrganizationSimpleViewset
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'programs', ProgramViewset)
program_router = routers.NestedDefaultRouter(router, r'programs', lookup='program')
program_router.register(r'invites', NestedProgramInviteViewset, basename='program-invites')
program_router.register(r'subscribers', NestedSubscribersViewset, basename='program-subscribers')

router.register(r'program_invites', ProgramInviteViewset)
router.register(r'associated_programs_organizations', ProgramInvitedOrganizationViewset)

router.register(r'organizations', OrganizationSimpleViewset, basename='organization')
organizations_router = routers.NestedDefaultRouter(router, r'organizations', lookup='organization')
organizations_router.register(r'programs', NestedOrganizationProgramViewset, basename='organization-programs')
organizations_router.register(r'invites', NestedOrganizationInviteViewset, basename='organization-invites')
organizations_router.register(r'associated_programs', NestedOrganizationAssociatedProgramViewset, basename='organization-associated-programs')

router.register(r'subscribers', UserSimpleViewset, basename='subscribers')
subscribers_router = routers.NestedDefaultRouter(router, r'subscribers', lookup='subscriber')
subscribers_router.register(r'programs', NestedSubscribedProgramsViewset, basename='subscribed-programs')



urlpatterns = [
    path('', include(router.urls)),
    path('', include(organizations_router.urls)),
    path('', include(program_router.urls)),
    path('', include(subscribers_router.urls))
]
