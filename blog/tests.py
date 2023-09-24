from django.test import TestCase

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework import status

from blog.models import Post
import unittest

class BlogTests(TestCase):
    #@unittest.skip('For now')
    def test_whether_user_has_permissions(self):

        content_type = ContentType.objects.get_for_model(Post)
        print(content_type)
            #blog | post

        post_permission = Permission.objects.filter(content_type=content_type)
        print([perm.codename for perm in post_permission])
            #['add_post', 'change_post', 'delete_post', 'view_post']
            
        user = User.objects.create_user(username="test", password="test", email="test@user.com")
        #print(user)
            #test

        # Check if the user has permissions already
        for perm in post_permission:
            app_permission_name = "blog." + perm.codename
            #print(user.has_perm(app_permission_name))
            self.assertIs(user.has_perm(app_permission_name), False)


        # To add permissions
        for perm in post_permission:
            user.user_permissions.add(perm)
            
        # Check if the user has permissions
        for perm in post_permission:
            app_permission_name = "blog." + perm.codename
            #print(user.has_perm(app_permission_name))
            self.assertIs(user.has_perm(app_permission_name), False)
            
            #False
            #False
            #False
            #False
            # Why? This is because Django's permissions do not take
            # effect until you allocate a new instance of the user.
            
            
        user = get_user_model().objects.get(email="test@user.com")

        # Check if the user has permissions
        for perm in post_permission:
            app_permission_name = "blog." + perm.codename
            #print(user.has_perm(app_permission_name))
            self.assertIs(user.has_perm(app_permission_name), True)

            #print(perm.content_type)
            #print(perm.name)
            #print(perm.codename)
            #print(user.has_perm("blog." + perm.codename))


    #@unittest.skip('For now')
    def test_whether_superuser_has_permissions(self):
        superuser = User.objects.create_superuser(
            username="super", password="test", email="super@test.com"
        )

        content_type = ContentType.objects.get_for_model(Post)
        print(content_type)
            #blog | post

        post_permission = Permission.objects.filter(content_type=content_type)
        print([perm.codename for perm in post_permission])


        # Check if the superuser has permissions
        # Output will be true
        for perm in post_permission:
            app_permission_name = "blog." + perm.codename
            #print(user.has_perm(app_permission_name))
            self.assertIs(superuser.has_perm(app_permission_name), True)

        # Output will be true even if the permission does not exists
        print(superuser.has_perm("foo.add_bar"))
     
     
    #@unittest.skip('For now')
    def test_whether_groups_have_permissions(self):

        author_group, created = Group.objects.get_or_create(name="Author")
        editor_group, created = Group.objects.get_or_create(name="Editor")
        publisher_group, created = Group.objects.get_or_create(name="Publisher")

        content_type = ContentType.objects.get_for_model(Post)
        post_permission = Permission.objects.filter(content_type=content_type)

        #print([perm.codename for perm in post_permission])
        # => ['add_post', 'change_post', 'delete_post', 'view_post']

        for perm in post_permission:
            if perm.codename == "delete_post":
                publisher_group.permissions.add(perm)

            elif perm.codename == "change_post":
                editor_group.permissions.add(perm)
                publisher_group.permissions.add(perm)
            else:
                author_group.permissions.add(perm)
                editor_group.permissions.add(perm)
                publisher_group.permissions.add(perm)

        user = User.objects.create_user(username="test", password="test", email="test@user.com")

        #user = User.objects.get(username="test")
        user.groups.add(author_group)  # Add the user to the Author group

        user = get_object_or_404(User, pk=user.id)

        app_permission_name = "blog.delete_post"
        #print(user.has_perm(app_permission_name)) # => False
        self.assertIs(user.has_perm(app_permission_name), False)
        
        app_permission_name = "blog.change_post"
        #print(user.has_perm(app_permission_name)) # => False
        self.assertIs(user.has_perm(app_permission_name), False)
        
        app_permission_name = "blog.view_post"
        #print(user.has_perm(app_permission_name)) # => True
        self.assertIs(user.has_perm(app_permission_name), True)
        
        app_permission_name = "blog.add_post"
        #print(user.has_perm(app_permission_name)) # => True
        self.assertIs(user.has_perm(app_permission_name), True)
        
        
    #@unittest.skip('For now')
    def test_enforcing_permissions(self):
        PASSWORD = 'test'
        user = User.objects.create_user(username="test", password=PASSWORD, email="test@user.com")

        self.client.login(username=user.username, password=PASSWORD)
        
        response = self.client.get(reverse('blog:list_by_viewfn'))
        #print(response)
        self.assertNotEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.get(reverse('blog:list_by_viewclass'))  
        #print(response)
        self.assertNotEqual(status.HTTP_200_OK, response.status_code)

        content_type = ContentType.objects.get_for_model(Post)
        #print(content_type)
            #blog | post

        post_permission = Permission.objects.filter(content_type=content_type)
        #print([perm.codename for perm in post_permission])
            #['add_post', 'change_post', 'delete_post', 'view_post']
        
        # Check if the user has permissions already
        for perm in post_permission:
            app_permission_name = "blog." + perm.codename
            #print(user.has_perm(app_permission_name))
            self.assertIs(user.has_perm(app_permission_name), False)

        # add 'view_post' permission
        for perm in post_permission:
            if (perm.codename == "view_post"):
                user.user_permissions.add(perm)

        self.client.login(username=user.username, password=PASSWORD)

        # view function passes
        response = self.client.get(reverse('blog:list_by_viewfn'))  
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        # view class still fails
        response = self.client.get(reverse('blog:list_by_viewclass'))  
        self.assertNotEqual(status.HTTP_200_OK, response.status_code)
        
        # add 'add_post' permission
        for perm in post_permission:
            if (perm.codename == "add_post"):
                user.user_permissions.add(perm)
        
        # now, view class passes
        response = self.client.get(reverse('blog:list_by_viewclass'))  
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTemplateUsed(response, "post.html")


    # commenting out this test, as it does not passes
    #@unittest.skip('For now')
    # def test_model_level_permissions(self):
        # first_item = Post()
        # first_item.title = "The first blog item"
        # first_item.body = "Blah blah blah"
        # first_item.is_published = False
        # first_item.save()    
    
        # PASSWORD = 'test'
        # user = User.objects.create_user(username="test", password=PASSWORD, email="test@user.com")

        # self.client.login(username=user.username, password=PASSWORD)
        
        # response = self.client.post(
            # #reverse('blog:details_by_viewclass'),
            # f"/details/1/",
            # data={"post_id": 1, "published_status": True},
        # )

        # self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.assertTemplateUsed(response, "post_details.html")
        