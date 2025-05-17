from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models.query import QuerySet

from . import models, forms


def index(request):
    return render(request, 'ads/index.html')


def get_all_ads(request):
    all_ads = models.Ad.objects.all()
    return render(request, 'ads/ads.html', {'ads': all_ads})


def create_ad(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.CreateAdForm(request.POST)
            if form.is_valid():
                ad = form.save(commit=False)
                ad.user = request.user
                ad.save()
                return JsonResponse({'status': 200})
            else:
                return HttpResponse(status=500, content='Не все поля заполнены верно!')
        else:
            form = forms.CreateAdForm()
            context = {'form': form}
            return render(request, "ads/create_ad.html", context)
    else:
        return redirect('login')


def edit_ad(request, ad_id: int):
    if request.user.is_authenticated:
        ad = models.Ad.objects.filter(id=ad_id)
        if ad:
            ad = ad[0]
            if ad.user == request.user:
                if request.method == 'POST':
                    form = forms.EditAdForm(request.POST, instance=ad)
                    if form.is_valid():
                        form.save()
                        return JsonResponse({'status': 200})
                    else:
                        return HttpResponse(status=500, content='Не все поля заполнены верно!')
                else:
                    default_values = {
                        'title': ad.title,
                        'description': ad.description,
                        'category': ad.category,
                        'condition': ad.condition
                    }
                    form = forms.EditAdForm(initial=default_values)
                    context = {'form': form,
                               'ad': ad}
                    return render(request, "ads/edit_ad.html", context)
            else:
                return HttpResponse(status=500, content='Вы не автор этого объявления!')
        else:
            return HttpResponse(status=404, content='Объявление не найдено!')
    else:
        return redirect('login')


def delete_ad(request, ad_id: int):
    if request.user.is_authenticated:
        ad = models.Ad.objects.filter(id=ad_id)
        if ad:
            ad = ad[0]
            if ad.user == request.user:
                ad.delete()
                return JsonResponse({'status': 200})
            else:
                return HttpResponse(status=500, content='Вы не автор этого объявления!')
        else:
            return HttpResponse(status=404, content='Объявление не найдено!')
    else:
        return redirect('login')


def search_ads(ads: QuerySet, key_word: str):
    pass


def filter_ads(ads: QuerySet, category: str, condition: str):
    pass


def get_ads(request, key_word: str = None, category: str = None, condition: str = None, len_page: int = 10, page_n: int = 1):
    pass


def create_proposal(request, ad_r_id: int):
    if request.user.is_authenticated:
        ad_r = models.Ad.objects.filter(id=ad_r_id)
        if ad_r:
            ad_r = ad_r[0]
            if request.method == 'POST':
                form = forms.CreateProposalForm(request.POST)

                if form.is_valid():
                    
                    prop = form.save(commit=False)
                    prop.ad_receiver = ad_r
                    prop.save()
                    return JsonResponse({'status': 200})
                else:
                    return HttpResponse(status=500, content='Не все поля заполнены верно!')
            else:
                form = forms.CreateProposalForm()
                ads = models.Ad.objects.filter(user=request.user)
                form.fields['ad_sender'].queryset = ads
                context = {'form': form,
                           'ad_r': ad_r}
                return render(request, "ads/create_prop.html", context)
        else:
            return HttpResponse(status=404, content='Объявление не найдено!')
    else:
        return redirect('login')


def accept_proposal(request, prop_id: int):
    if request.user.is_authenticated:
        prop = models.Proposal.objects.filter(id=prop_id)
        if prop:
            prop = prop[0]
            if prop.ad_receiver.user == request.user:
                prop.status = 'принято'
                prop.save()
                return JsonResponse({'status': 200})
            else:
                return HttpResponse(status=500, content='Предложение адресовано не вам!')
        else:
            return HttpResponse(status=404, content='Предложение не найдено!')
    else:
        return redirect('login')


def reject_proposal(request, prop_id: int):
    if request.user.is_authenticated:
        prop = models.Proposal.objects.filter(id=prop_id)
        if prop:
            prop = prop[0]
            if prop.ad_receiver.user == request.user:
                prop.status = 'отклонено'
                prop.save()
                return JsonResponse({'status': 200})
            else:
                return HttpResponse(status=500, content='Предложение адресовано не вам!')
        else:
            return HttpResponse(status=404, content='Предложение не найдено!')
    else:
        return redirect('login')

def filter_proposals(proposals: QuerySet):
    pass


def get_proposals(request):
    pass