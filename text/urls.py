from django.urls import path, re_path

from text import views

app_name = 'text'

urlpatterns = [
    path('ciphermessage/', views.cipherMessage, name = "cipherMessage"),
    path('ciphermessage/api/', views.CipherMessageApi.as_view(), name = "cipherMessageApi"),
    path('commonword/', views.commonWord, name = "commonWord"),
    path('commonword/api/', views.CommonWordApi.as_view(), name = "CommonWordApi"),
    path('formattabindent/', views.formatTabIndent, name = "formatTabIndent"),
    path('formattabindent/api/', views.FormatTabIndentApi.as_view(), name = "formatTabIndentApi"),
    path('generatecode/', views.generateCode, name = "generateCode"),
    path('limitlinelength/', views.limitLineLength, name = "limitLineLength"),
    path('', views.text, name = "textRoot"),
]
