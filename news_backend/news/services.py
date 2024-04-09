import requests
from django.contrib.auth.models import User
from .models import Story, Comment
#services file created to implement particular functionality such as bookmarkingand other things
NEWS_API_KEY = '21d7afb2b0bd4006aa6b43f6ac7f1051'

def fetch_stories(category):#fetches stories according to categories
    categories = {
        'top': 'top-headlines?country=us',
        'best': 'top-headlines?country=us&category=business',
        'new': 'everything?q=news'
    }
    if category not in categories:
        return {'error': f'Invalid category: {category}'}

    url = f'https://newsapi.org/v2/{categories[category]}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        
        # Save stories to the database
        for article in articles:
            title = article.get('title', '')
            author = article.get('author', '')
            content = article.get('content', '')
            created_at = article.get('createdAt', '')
            
            # Create a new Story instance and save it to the database
            Story.objects.create(title=title, author=author, content=content, published_at=published_at)
            
        return {'stories': articles}
    else:
        return {'error': f'Failed to fetch stories: {response.status_code}'}
def fetch_comments_for_story(story_id):#fetches comments of a story
    try:
        comments = Comment.objects.filter(story=story_id)
        serialized_comments = [{
            'id': comment.id,
            'text': comment.text,
            'created_at': comment.created_at
        } for comment in comments]
        return serialized_comments
    except Exception as e:
        print(f"Error fetching comments for story {story_id}: {e}")
        return []
def search_stories(query):#searches stories
    stories = Story.objects.filter(title__icontains=query)
    serialized_stories = [{'title': story.title, 'author': story.author, 'created_at': story.created_at} for story in stories]
    return serialized_stories
def search_comments(query):#searches comments
    comments=Comment.objects.filter(text__icontains=query)
    serialized_comments=[{'story': comment.story, 'author': comment.author, 'comment_text':comment.text,'created_at': comment.created_at} for comment in comments]
    return serialized_comments
def bookmark_story(user, story_id):
    try:
        story = Story.objects.get(id=story_id)
        user.userprofile.bookmarked_stories.add(story)
        return True
    except Story.DoesNotExist:
        return False

def bookmark_comment(user, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        user.userprofile.bookmarked_comments.add(comment)
        return True
    except Comment.DoesNotExist:
        return False