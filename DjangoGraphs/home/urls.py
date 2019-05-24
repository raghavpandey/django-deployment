from django.urls import path
from .views import HomeView, UserView, ReportView, MonthView, SuccessView, PredictView, SocView, ReviewView, RegDurPageView, SocTypeView

urlpatterns = [
    path('', HomeView.as_view(), name='HomePageView'),
    path('SocAnalysis', SocView.as_view(), name='SocietyPageView'),
    path('UserAnalysis', UserView.as_view(), name='UserPageView'),
    path('ReportAnalysis', ReportView.as_view(), name='ReportPageView'),
    path('MonthAnalysis', MonthView.as_view(), name='MonthPageView'),
    # path('MonthAnalysis', CurrMonthView.as_view(), name='CurrMonthPageView'),
    path('PredictiveAnalysis', PredictView.as_view(), name='PredictPageView'),
    path('Reviews', ReviewView.as_view(), name='ReviewPageView'),
    path('RegDuration', RegDurPageView.as_view(), name='RegDurPageView'),
    path('SocType', SocTypeView.as_view(), name='SocietyTypePageView'),
    path('success', SuccessView.as_view(), name='portal_SuccessView'),
]
