from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin

from mainapp.models import User


class Stop(MiddlewareMixin):
    def process_request(self,req):
        path = req.path
        if path.find('/cart') == 0:
            user = User.objects.filter(token=req.COOKIES.get('token'))
            print(user)
            if not user:
                return redirect('/login')