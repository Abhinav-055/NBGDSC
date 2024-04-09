from django.urls import path
from .views import (top_stories,search_comment, comments_for_story, user_profile, search,bookmark_story_view, bookmark_comment_view,best_stories,new_stories)

urlpatterns = [
    path('top-stories/', top_stories, name='top_stories'),
    path('comments/<str:story_id>/', comments_for_story, name='comments_for_story'),
    path('user/<str:username>/', user_profile, name='user_profile'),
    path('search/', search, name='search'),
    path('search_comment',search_comment),
    path('bookmark/story/<int:story_id>/', bookmark_story_view, name='bookmark_story'),
    path('bookmark/comment/<int:comment_id>/', bookmark_comment_view, name='bookmark_comment'),
    path('best-stories/', best_stories, name='best_stories'),
    path('new-stories/', new_stories, name='new_stories'),
]