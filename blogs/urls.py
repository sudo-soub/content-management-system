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
        views.BlogsRetrieveUpdateView.as_view({
            'get': 'retrieve'
        }),
        name="retrieve-update-blog"
    ),
    path(
        'myblogs/',
        views.GetUpdateBlogsByUser.as_view(),
        name="get-update-blogs-by-user"
    )
]