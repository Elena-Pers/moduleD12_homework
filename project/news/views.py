from django.shortcuts import render
 # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import News
from datetime import datetime
from .filters import NewsFilter # импортируем недавно написанный фильтр
from .forms import NewsForm
from django.core.paginator import Paginator


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

class NewsCreate(CreateView):
        template_name = 'create.html'
        form_class = NewsForm


# дженерик для редактирования объекта
class NewsUpdateView(UpdateView):
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




