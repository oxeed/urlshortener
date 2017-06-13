from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, Http404, HttpResponseRedirect

from .forms import SumbitUrlForm
from .models import ShortURL
from analytics.models import ClickEvent
# Create your views here.


"""def shorturl_redirect_view(request, shortcode=None, *args, **kwargs):
     3 random options how can write views in function style:
     try: except:
     with queryset
     with get_objects_or_404 - the best practice in this tutorial.

     1) obj = ShortURL.objects.get(shortcode=shortcode)
     try:
        obj = ShortURL.objects.get(shortcode=shortcode)
     except:
        obj = ShortURL.objects.all().first()


     2)   obj_url = None
     qs = ShortURL.objects.filter(shortcode__iexact=shortcode())
     if qs.exists()and qs.count() == 1:
        obj = qs.first()
        obj_url = obj.url

     3) obj = get_object_or_404(ShortURL, shortcode=shortcode)
     return HttpResponse("hello {sc}".format(sc=obj.url))"""


class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = SumbitUrlForm()
        context = {
            "form": form,
        }
        return render(request, 'shortener/home.html', context)

    def post(self, request, *args, **kwargs):
        form = SumbitUrlForm(request.POST)
        context = {
            'form': form,
        }
        template = 'shortener/home.html'

        if form.is_valid():
            new_url = form.cleaned_data.get('url')
            obj, created = ShortURL.objects.get_or_create(url=new_url)
            context = {
                'object': obj,
                'created': created
            }
            if created:
                template = 'shortener/success.html'
            else:
                template = 'shortener/already-exists.html'

        return render(request, template, context)


class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        # obj = get_object_or_404(ShortURL, shortcode=shortcode)
        qs = ShortURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() == 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)



