
from django.urls import path
from . import views


urlpatterns = [
    path('negotiations/', views.NegotiationListView.as_view(), name='negotiation-list'),
    # http://127.0.0.1:8000/guest/api/nego/negotiation_details/${negotiationId}/`, {
    path('negotiation_details/<int:negotiation_id>/', views.NegotiationDetailsView.as_view(), name='negotiation-details'),
    path('offer_accepted_by_guest/', views.OfferAcceptedByGuestView.as_view(), name='offer-accepted-by-guest'),
    path('offer_rejected_by_guest/', views.OfferRejectedByGuestView.as_view(), name='offer-rejected-by-guest'),

]
 