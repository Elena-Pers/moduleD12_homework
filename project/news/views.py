
 # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import News, Category
from datetime import datetime
from .filters import NewsFilter # импортируем недавно написанный фильтр
from .forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Appointment
from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse_lazy, resolve
from django.template.loader import render_to_string
from django.conf import settings


class NewsList(ListView):
    model = News  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    #queryset = News.objects.order_by('-id')
    queryset = News.objects.order_by('-creationTime')
    paginate_by = 10  # поставим постраничный вывод в один элемент

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)

# создаём представление, в котором будут детали конкретного отдельного товара
class NewsDetail(DetailView):
    model = News  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'new.html'  # название шаблона будет product.html
    context_object_name = 'new'  # название объекта


from django.shortcuts import render

# Create your views here.
class NewsSearch(ListView):
    model = News
    template_name = 'search.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'newsSearch'
    queryset = News.objects.order_by('-creationTime')
    #paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET,
        queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

class NewsCreate(PermissionRequiredMixin, CreateView):
        permission_required = ('news.add_news',)
        template_name = 'create.html'
        form_class = NewsForm




# дженерик для редактирования объекта
class NewsUpdateView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = ('news.change_news',)
    template_name = 'create.html'
    form_class = NewsForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return News.objects.get(pk=id)



# дженерик для удаления товара
class NewsDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = News.objects.all()
    context_object_name = 'new'
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/')


class PostCategoryView(ListView):
     model = News
     template_name = 'news_app/category.html'
     context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
     # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
     ordering = ['-dateCreation']  # сортировка
     paginate_by = 10  # поставим постраничный вывод в один элемент

     def get_queryset(self):
         self.id = resolve(self.request.path_info).kwargs['pk']
         c = Category.objects.get(id=self.id)
         queryset = News.objects.filter(category_id=c)

         return queryset

     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         user = self.request.user
         category = Category.objects.get(id=self.id)
         subscribed = category.subscribers.filter(email=user.email)
         if not subscribed:
             context['category'] = category
         return context


@login_required
def subscribe_to_category(request, pk):  # подписка на категорию
     user = request.user
     category = Category.objects.get(id=pk)

     if not category.subscribers.filter(id=user.id).exists():
         category.subscribers.add(user)
         email = user.email
         html = render_to_string(
             'mail/subscribed.html',
             {
                 'category': category,
                 'user': user,
             },
         )
         msg = EmailMultiAlternatives(
             subject=f'Подписка на {category} на сайте News Paper',
             body='',
             from_email='lena_zaika_nsk@mail.ru',  # в settings.py
             to=[email, ],  # список получателей
         )
         msg.attach_alternative(html, 'text/html')

         try:
             msg.send()
         except Exception as e:
             print(e)
         return redirect('/news/subscribed/', category=category)
         # return redirect('news_list')
     return redirect('/news/subscribed/', { 'category': category })  # возвращает на страницу, с кот-й поступил запрос


@login_required
def unsubscribe_from_category(request, pk):  # отписка от категории
     user = request.user
     c = Category.objects.get(id=pk)

     if c.subscribers.filter(id=user.id).exists():  # проверяем есть ли у нас такой подписчик
         c.subscribers.remove(user)  # то удаляем нашего пользователя
     # return redirect('http://127.0.0.1:8000/')
     return redirect('/news/unsubscribed/')


class AppointmentView(View):
     def get(self, request, *args, **kwargs):
         return render(request, 'news_app/make_app.html', {})

     def post(self, request, *args, **kwargs):
         appointment = Appointment(
             date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
             client_name=request.POST['client_name'],
             message=request.POST['message'],
         )
         appointment.save()

         return redirect('news:make_app')