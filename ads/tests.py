from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from .models import Ad, Proposal


class AdTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Объявление 1',
            description='Описание 1',
            category='вещи для дома',
            condition='новый'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Объявление 2',
            description='Описание 2',
            category='одежда',
            condition='б/у'
        )

    def test_ad_creation(self):
        self.client.login(username='user1', password='password1')
        url = reverse('create_ad')
        data = {
            'title': 'Новое объявление',
            'description': 'Описание нового объявления',
            'category': 'транспорт', 
            'condition': 'б/у'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ad.objects.count(), 3)
        new_ad = Ad.objects.latest('id')
        self.assertEqual(new_ad.title, 'Новое объявление')
        self.assertEqual(new_ad.user, self.user1)
        self.assertEqual(new_ad.category, 'транспорт')

    def test_ad_editing(self):
        self.client.login(username='user1', password='password1')
        url = reverse('edit_ad', args=[self.ad1.id])
        data = {
            'title': 'Обновленный заголовок',
            'description': 'Обновленное описание',
            'category': 'одежда',
            'condition': 'новый'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.ad1.refresh_from_db()
        self.assertEqual(self.ad1.title, 'Обновленный заголовок')
        self.assertEqual(self.ad1.category, 'одежда')

    def test_ad_deletion(self):
        self.client.login(username='user1', password='password1')
        url = reverse('delete_ad', args=[self.ad1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ad.objects.count(), 1)
        self.assertFalse(Ad.objects.filter(id=self.ad1.id).exists())

    def test_get_ads_paginated(self): 
        url = reverse('get_all_ads', args=[1]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  

        self.assertContains(response, self.ad1.title)
        self.assertContains(response, self.ad2.title)

        url = reverse('get_all_ads', args=[2]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ProposalTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Объявление 1',
            description='Описание 1',
            category='вещи для дома',
            condition='новый'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Объявление 2',
            description='Описание 2',
            category='одежда',
            condition='б/у'
        )
        self.proposal1 = Proposal.objects.create(
            ad_sender=self.ad2,
            ad_receiver=self.ad1,
            comment='Комментарий'
        )

    def test_proposal_creation(self):
        self.client.login(username='user2', password='password2')
        url = reverse('create_prop', args=[self.ad1.id])
        data = {
            'ad_sender': self.ad2.id,
            'comment': 'Комментарий к обмену'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Proposal.objects.count(), 2)
        new_proposal = Proposal.objects.latest('id')
        self.assertEqual(new_proposal.ad_receiver, self.ad1)
        self.assertEqual(new_proposal.ad_sender, self.ad2)
        self.assertEqual(new_proposal.comment, 'Комментарий к обмену')

    def test_proposal_accept(self):
        self.client.login(username='user1', password='password1') 
        url = reverse('accept_prop', args=[self.proposal1.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)
        self.proposal1.refresh_from_db()
        self.assertEqual(self.proposal1.status, 'принято')

    def test_proposal_reject(self):
        self.client.login(username='user1', password='password1') 
        url = reverse('reject_prop', args=[self.proposal1.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)
        self.proposal1.refresh_from_db()
        self.assertEqual(self.proposal1.status, 'отклонено')

    def test_get_proposals(self):
         self.client.login(username='user1', password='password1')
         url = reverse('get_all_props')
         response = self.client.get(url)
         self.assertEqual(response.status_code, 200)
