from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from blog_app.models import Post, Comment
from blog_app.forms import PostForm, CommentForm
from django.views.generic import (TemplateView, ListView,
                                    DetailView, CreateView,
                                    UpdateView, DeleteView )
# Create your views here.


class AboutView(TemplateView):
    template_name = 'blog_app/about.html'

class PostListView(ListView):
    model = Post
    
    def get_queryset(self):
        # __lte = lessthen or equal
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "blog_app/post_detail.html"
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "blog_app/post_detial.html"
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog_app:post_list") 


class DraftListView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "blog_app/post_list.html"
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('create_date')




###################################################################################################################
###################################################################################################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.publish()
    return redirect("blog_app:post_detail", pk = pk)


    
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect("blog_app:post_detail", pk = post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog_app/comment_form.html', {'form' : form})        

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    comment.approve()
    return redirect('blog_app:post_detail', pk = comment.post.pk)     


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk = pk) #fetch the "comment" object from the database using primary key (pk) provided in the url

    #if request.user != comment.author and request.user != comment.post.author:  #it is accessible by post_user and comment_user to delete...
    # if request.user != comment.author:
    #     return HttpResponseForbidden("You are not allowed to delete this  comment.")

    post_pk = comment.post.pk #save the key in seperate veriable
    comment.delete()
    return redirect("blog_app:post_detail", pk = post_pk)
