from django.views.generic import ListView
from cuser_app.models import CustomUser

# Create your views here.
class HomeView(ListView):
    template_name = "home_app/home.html"
    #model = CustomUser
    context_object_name = "users_list"

    def get_queryset(self):
        curr_user = self.request.user.id
        return CustomUser.objects.exclude(id=curr_user)




    