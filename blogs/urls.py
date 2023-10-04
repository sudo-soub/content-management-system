from django.urls import path
from blogs import views

urlpatterns = [
    path(
        'blog',
        views.BlogsGetPostView.as_view(),
        name="get-post-blog"
    ),
    path(
        'blog/<str:pk>',
        views.BlogsRetrieveUpdateView.as_view(),
        name="retrieve-update-blog"
    )
]