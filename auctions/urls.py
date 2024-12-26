from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add",views.listing_page, name="add"),
    path("<int:listing_id>", views.listing_view,name="view"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categoriesf, name="categories"),
    path("category/<str:category_name>",views.category_name,name="category_name"),
    path("close/<int:listing_id>", views.close_auction, name="close_auction"),
    path("closed",views.closed, name  ="closed")
]
