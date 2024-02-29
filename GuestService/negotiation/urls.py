
from django.urls import path
from . import views


urlpatterns = [
    path('negotiations/as_guest/', views.NegotiationAsGuestView.as_view(), name='negotiation-as-guest'),
    path('negotiations/as_host/', views.NegotiationAsHostView.as_view(), name='negotiation-as-host'),
    path('update_status/<int:negotiation_id>/', views.UpdateStatusView.as_view(), name='update-status'),
    path('negotiations/', views.NegotiationListView.as_view(), name='negotiation-list'),
    path('host_proposed/<int:negotiation_id>/', views.HostProposedView.as_view(), name='host-proposed'),
    
    path('negotiation_details/<int:negotiation_id>/', views.NegotiationDetailsView.as_view(), name='negotiation-details'),
    path('offer_accepted_by_guest/', views.OfferAcceptedByGuestView.as_view(), name='offer-accepted-by-guest'),
    path('offer_rejected_by_guest/', views.OfferRejectedByGuestView.as_view(), name='offer-rejected-by-guest'),
    path('offer_accepted_by_host/', views.OfferAcceptedByHostView.as_view(), name='offer-accepted-by-host'),
    path('offer_rejected_by_host/', views.OfferRejectedByHostView.as_view(), name='offer-rejected-by-host'),
    path('start_negotiation_by_guest/', views.StartNegotiationByGuestView.as_view(), name='start-negotiation-by-guest'),

]
 