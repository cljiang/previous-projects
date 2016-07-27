import cStringIO as StringIO

from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.utils import timezone
from .models import Post, Comment, Document, Album, Photo, mylist
from .forms import PostForm, CommentForm, DocumentForm, AlbumForm, PhotoForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from braces.views import AjaxResponseMixin, JSONResponseMixin, LoginRequiredMixin,SuperuserRequiredMixin
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)

def upload_document(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(post=post, docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('blog.views.upload_document', pk=post.pk))
            return redirect('blog.views.upload_document', pk=post.pk)
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form, 'post': post},
        context_instance=RequestContext(request)
    )

def myview(request, pk):
    post = get_object_or_404(Post, pk=pk)
    print(request.POST)
    return render_to_pdf(
         'blog/post_detail.html',
         {
            'pagesize':'A4',
            'post': post,
         }
        )

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = StringIO.StringIO()

    print("========> ", html.encode("utf-8"))
    # pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    print(pdf)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('we had some errors<pre>%s</pre>' % escape(html))

class AjaxPhotoUploadView(LoginRequiredMixin,SuperuserRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self,request,pk):
        try:
            album = Album.objects.get(pk)
        except Album.DoesNotExist:
            error_dict = {'message': 'Album not found.'}
            return self.render_json_response(error_dict,status=404)

        uploaded_file = request.FILES['photofile']
        Photo.objects.create(album=album,file=uploaded_file)

        response_dict = {
            'message': 'File uploaded successfully!',
        }

        return self.render_json_response(response_dict,status=200)

