from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from .forms import UserRegisterForm, UserLoginForm
import requests


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class RegisterPageView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'auth/register.html', {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            url = 'http://127.0.0.1:8001/users/register'
            data = {
                "username": username,
                "email": email,
                "password": password
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return HttpResponse("User registered successfully!")
            else:
                return HttpResponse(f"Error: {response.json()['detail']}")
        else:
            form = UserRegisterForm()
            return render(request, 'auth/register.html', {'form': form})


class UserLoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            api_url = 'http://127.0.0.1:8001/users/login/'

            data = {
                "username_or_email": username_or_email,
                "password": password
            }
            response = requests.post(api_url, json=data)

            if response.status_code == 200:
                return JsonResponse({'message': 'User registered successfully!', 'data': response.json()})
            else:
                return JsonResponse({'error': 'Failed to login user', 'details': response.json()},
                                    status=response.status_code)


class UserGetView(View):

    def get(self, request, *args, **kwargs):
        page = requests.get("http://127.0.0.1:8001/users/?size=1").json()['page']
        pages = requests.get("http://127.0.0.1:8001/users/?size=1").json()["pages"]

        if page is not None:
            if int(page) <= int(pages):
                data = requests.get("http://127.0.0.1:8001/users/?size=1").json()["items"]
                return render(request, "users.html",
                              context={"users": data, "pages": pages, "page": page, "next": int(page) + 1,
                                       "previous": int(page) - 1})

            data = requests.get(f"http://127.0.0.1:8001/users/?page={page}&size=1").json()["items"]
            return render(request, "users.html",
                          context={"users": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "users.html", context={"message": "Not found"})


class PostGetView(View):
    def get(self, request):
        return render(request, 'post.html')

    def post(self, request):
        caption = request.POST.get('caption')
        image_path = request.POST.get('image_path')

        api_url = 'http://127.0.0.1:8001/posts/create'

        data = {
            "caption": caption,
            "image_path": image_path
        }

        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            return render(request, 'post.html')

        else:
            return JsonResponse({'error': 'Failed to login user', 'details': response.json()},
                                status=response.status_code)

    def get(self, request, *args, **kwargs):
        page = requests.get("http://127.0.0.1:8001/posts/?size=2").json()['page']
        pages = requests.get("http://127.0.0.1:8001/posts/?size=2").json()["pages"]

        if page is not None:
            if int(page) <= int(pages):
                data = requests.get(f"http://127.0.0.1:8001/posts/?size=2").json()["items"]
                return render(request, "post.html",
                              context={"posts": data, "pages": pages, "page": 1, "next": 2, "previous": 0})

            data = requests.get(f"http://127.0.0.1:8001/posts/?page={page}&size=2").json()["items"]
            return render(request, "post.html",
                          context={"posts": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "post.html", context={"message": "Not found"})


class CommentGetView(View):
    def get(self, request):
        return render(request, 'comment.html')

    def post(self, request):
        content = request.POST.get('content')

        api_url = 'http://127.0.0.1:8001/comments/create'

        data = {
            "content": content,
        }

        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            return render(request, 'comment.html')

        else:
            return JsonResponse({'error': 'Failed to login user', 'details': response.json()},
                                status=response.status_code)

    def get(self, request, *args, **kwargs):
        page = requests.get(f"http://127.0.0.1:8001/comments/?size=1").json()['page']
        pages = requests.get(f"http://127.0.0.1:8001/comments/?size=1").json()["pages"]

        if page is not None:
            if int(page) <= int(pages):
                data = requests.get(f"http://127.0.0.1:8001/comments/?size=1").json()["items"]
                return render(request, "comment.html",
                              context={"comments": data, "pages": pages, "page": 1, "next": 2, "previous": 0})

            data = requests.get(f"http://127.0.0.1:8001/comments/?page={page}&size=1").json()["items"]
            return render(request, "comment.html",
                          context={"comments": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "comment.html", context={"message": "Not found"})
