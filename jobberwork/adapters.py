from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import User

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        u = sociallogin.user
        if not u.email.split('@')[1] == "vitstudent.ac.in":
            return Response({"error": "Login with your vit student id"})

'''
{
    "access_token": "",
    "code": "4/0AY0e-g6RQ7sOfUSSgt1Wc2aEUePrgo1z8-wFzoWzcomCyiW62_2ho5btPGlRowNv7dIH-A",
"callback_url": "http://127.0.0.1:8000/"
}
'''