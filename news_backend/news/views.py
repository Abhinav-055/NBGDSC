from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .services import fetch_stories, fetch_comments_for_story,search_stories,search_comments ,bookmark_story, bookmark_comment
@login_required
def top_stories(request):
    stories = fetch_stories('top')
    return JsonResponse(stories)
@login_required
def best_stories(request):
    stories = fetch_stories('best')
    return JsonResponse(stories)
@login_required
def new_stories(request):
    stories = fetch_stories('new')
    return JsonResponse(stories)
@login_required
def comments_for_story(request, story_id):
    return fetch_comments_for_story(story_id)
@login_required
def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = {
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
            'submissions_count': user.story_set.count(),  # Assuming Story is your submission model
            'comments_count': user.comment_set.count(),
            'karma_points': user.userprofile.karma_points  # Assuming UserProfile model is linked to User model
        }
        return JsonResponse(profile)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)
@login_required
def search(request):
    query = request.GET.get('q', '')
    results = search_stories(query)
    return JsonResponse(results)
def search_comment(request):
    query=request.GET.get('q', '')
    results=search_comments(query)
    return JsonResponse(results)
@login_required
def bookmark_story_view(request, story_id):
    if request.method == 'POST':
        bookmark_story(story_id)
        return JsonResponse({'message': 'Story bookmarked successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=405)
@login_required
def bookmark_comment_view(request, comment_id):
    if request.method == 'POST':
        bookmark_comment(comment_id)
        return JsonResponse({'message': 'Comment bookmarked successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=405)
