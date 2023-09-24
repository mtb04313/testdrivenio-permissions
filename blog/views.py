from django.shortcuts import render

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from blog.models import Post


@permission_required("blog.view_post")
def post_list_view(request):
    return HttpResponse("If you can read this, you've got 'blog.view_post' permission!")

    
class PostListView(PermissionRequiredMixin, ListView):
    permission_required = ("blog.view_post", "blog.add_post")
    template_name = "post.html"
    model = Post



from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View

class PostDetailsView(UserPassesTestMixin, View):
    template_name = "post_details.html"

    def test_func(self):
        return self.request.user.has_perm("blog.set_published_status")

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        print(post_id)
        published_status = request.POST.get('published_status')
        print(published_status)
        
        if post_id:
            post = Post.objects.get(pk=post_id)
            post.is_published = bool(published_status)
            post.save()

        return render(request, self.template_name)
        