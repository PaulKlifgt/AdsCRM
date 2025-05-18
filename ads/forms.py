from django import forms
from .models import Ad, Proposal

class CreateAdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ('title', 'description', 'category', 'condition')
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'condition': 'Состояние',
        }
    def __init__(self, *args, **kwargs):
        super(CreateAdForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
    

class EditAdForm(CreateAdForm):
    def __init__(self, *args, **kwargs):
        super(EditAdForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['description'].required = False
        self.fields['category'].required = False
        self.fields['condition'].required = False


class CreateProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('ad_sender', 'comment')
        labels = {
            'ad_sender': 'Предложить',
            'comment': 'Комментарий к обмену',
        }
    def __init__(self, *args, **kwargs):
        super(CreateProposalForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = False
        self.fields['ad_sender'].label_from_instance = lambda obj: "%s" % (obj.title)