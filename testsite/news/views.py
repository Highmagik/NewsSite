from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from .utils import MyMixin
from django.contrib.auth.forms import UserCreationForm


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('главная страница')
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    paginate_by = 2
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # pk_url_kwarg = 'news_id'
    # template_name = 'news_detail.html'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = reverse_lazy('home')
    raise_exception = True


class Register(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'news/register.html'
    success_message = 'Вы успешно зарегистрировались'
    error_message = 'Ошибка регистрации'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class UserLogin(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'news/login.html'
    redirect_field_name = 'home'
    success_message = 'Успешно'
    error_message = 'Неверный логин или пароль'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


def user_logout(request):
    logout(request)
    return redirect('login')

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = get_object_or_404(Category, pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})


# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


# def add_news(request):
#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
