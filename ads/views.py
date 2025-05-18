from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from . import models, forms
from users.models import User


@login_required
def create_ad(request):
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


@login_required
def edit_ad(request, ad_id: int):
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


@login_required
@require_http_methods(['POST'])
def delete_ad(request, ad_id: int):
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


def search_ads(ads: QuerySet, key_word: str) -> list:
    ads_list = list(ads)
    for ad in ads:
        if not (key_word in ad.title or key_word in ad.description):
            ads_list.remove(ad)
    return ads_list


def filter_ads(category: str, condition: str):
    if category and condition:
        return models.Ad.objects.filter(category=category, condition=condition)
    elif category:
        return models.Ad.objects.filter(category=category)
    elif condition:
        return models.Ad.objects.filter(condition=condition)
    else:
        return models.Ad.objects.all()


@require_http_methods(['GET'])
def get_ads(request, page_n: int = 1):
    category = request.GET.get('category')
    condition = request.GET.get('condition')
    key_word = request.GET.get('key_word')
    len_page = 10
    context = {'page_n': page_n}
    filtered_ads = filter_ads(category, condition)
    if key_word:
        filtered_ads = search_ads(filtered_ads, key_word)
    context['ads'] = filtered_ads[(len_page*(page_n-1)):(len_page*page_n)]
    return render(request, 'ads/ads.html', context)


@login_required
def create_proposal(request, ad_r_id: int):
    ad_r = models.Ad.objects.filter(id=ad_r_id)
    if ad_r:
        ad_r = ad_r[0]
        if ad_r.user != request.user:
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
            return HttpResponse(status=403, content='Нельзя обмениваться с самим собой!')
    else:
        return HttpResponse(status=404, content='Объявление не найдено!')


@login_required
@require_http_methods(['POST'])
def accept_proposal(request, prop_id: int):
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


@login_required
@require_http_methods(['POST'])
def reject_proposal(request, prop_id: int):
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


def filter_proposals(sender: User = None, receiver: User = None, status: str = None):
    props: QuerySet = models.Proposal.objects.all()
    props_list = list(props)
    if sender:
        for prop in props:
            if prop.ad_sender.user != sender:
                props_list.remove(prop)
    props: list = props_list
    if receiver:
        for prop in props:
            if prop.ad_receiver.user != receiver:
                props_list.remove(prop)
    props: list = props_list
    if status in ['ожидает', 'принято', 'отклонено']:
        for prop in props:
            if prop.status != status:
                props_list.remove(prop)
    return props_list


@login_required
@require_http_methods(['GET'])
def get_proposals(request):
    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    status = request.GET.get('status')
    context = {}
    if not (sender or receiver or status):
        context['props_sended'] = filter_proposals(sender=request.user, status=status)
        context['props_received'] = filter_proposals(receiver=request.user, status=status)
    else:
        context['props'] = filter_proposals(sender, receiver, status)
    return render(request, 'ads/proposals.html', context)