from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django import forms
from allauth.account.forms import SignupForm
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from msngr.models import Member


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='RegisteredUsers')
        basic_group.user_set.add(user)
        return user


class BaseRegisterForm(UserCreationForm):
    # additional fields
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Firstname')
    last_name = forms.CharField(label='Lastname')

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2', )


class ProfileForm(ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput)
    username = forms.CharField()


    class Meta:
        model = Member
        fields = ['username',
                  'avatar']

    def get_avatar_img(self, obj):
        return mark_safe('<img src="{url}" style="max-width:{width}; max-height:{height};" />'.format(
            url=obj.avatar.url,
            width='200px',
            height='200px',))

    # def clean_avatar(self):
    #     avatar = self.cleaned_data['avatar']
    #
    #     try:
    #         w, h = get_image_dimensions(avatar)
    #
    #         #validate dimensions
    #         max_width = max_height = 100
    #         if w > max_width or h > max_height:
    #             raise forms.ValidationError(
    #                 u'Please use an image that is '
    #                  '%s x %s pixels or smaller.' % (max_width, max_height))
    #
    #         #validate content type
    #         main, sub = avatar.content_type.split('/')
    #         if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
    #             raise forms.ValidationError(u'Please use a JPEG, '
    #                 'GIF or PNG image.')
    #
    #         #validate file size
    #         if len(avatar) > (20 * 1024):
    #             raise forms.ValidationError(
    #                 u'Avatar file size may not exceed 20k.')
    #
    #     except AttributeError:
    #         """
    #         Handles case when we are updating the user profile
    #         and do not supply a new avatar
    #         """
    #         pass
    #
    #     return avatar
