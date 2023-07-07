from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, NewsUpdateView, NewsDeleteView # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='news'),
    path('search/', NewsSearch.as_view()),
    path('add/', NewsCreate.as_view(), name='create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='delete'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
]


'''
urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', NewsList.as_view()),
    path('search', NewsSearch.as_view()),
    path('<int:pk>', NewsDetailView.as_view(), name='news'),
    path('add/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
]
'''