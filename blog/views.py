from django.shortcuts import redirect,render,get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from .forms import PostForm,CommentForm

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})
def post_detail(request, post_id):
	posts = get_object_or_404(Post, pk=post_id)
	return render(request, 'blog/post_detail.html', {'posts': posts})
@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			posts = form.save(commit=False)
			posts.author = request.user
			posts.save()
			return render(request, 'blog/post_detail.html', {'posts': posts})
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})  
@login_required
def post_edit(request, post_id):
	posts = get_object_or_404(Post, pk=post_id)
	if request.method == "POST":
		form = PostForm(request.POST, instance=posts)
		if form.is_valid():
			posts = form.save(commit=False)
			posts.author = request.user
			posts.save()
			return render(request, 'blog/post_detail.html', {'posts': posts})
	else:
		form = PostForm(instance=posts)
	return render(request, 'blog/post_edit.html', {'form': form})
@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})
@login_required
def post_publish(request,post_id):
	posts = get_object_or_404(Post,pk=post_id)
	posts.publish()
	return render(request, 'blog/post_detail.html', {'posts': posts})
@login_required
def post_remove(request,post_id):
	posts = get_object_or_404(Post,pk=post_id)
	posts.delete()
	return redirect('post_list')
def add_comment_to_post(request, post_id):
	posts = get_object_or_404(Post, pk=post_id)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = posts
			comment.save()
			return render(request, 'blog/post_detail.html', {'posts': posts})
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})
@login_required
def comment_approve(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	comment.approve()
	return redirect('post_detail', pk=comment.post.comment_id)
@login_required
def comment_remove(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	comment.delete()
	return redirect('post_detail', pk=comment.post.comment_id)