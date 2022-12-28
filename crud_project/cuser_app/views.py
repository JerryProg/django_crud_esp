from django.contrib.auth import views
from crud_project.forms import LoginForm
from django.views.generic import RedirectView, CreateView, edit
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate
from django.conf import settings
from django.urls import reverse_lazy
from cuser_app.models import CustomUser
from crud_project.forms import UserCreationForm, UpdateViewForm


# Create your views here.
class LoginView(views.LoginView):
    template_name = "cuser_app/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user=True


class LogoutView(RedirectView):
    url = reverse_lazy(settings.LOGOUT_REDIRECT_URL)
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class RegisterView(SuccessMessageMixin, CreateView):    
    model = CustomUser
    template_name = "cuser_app/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_message = "El usuario con el email %(email)s se ha creado con exito"
        
    #Register and login at the same time
    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        user = authenticate(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
        f_login = login(self.request, user)
        return valid


#UpdateView
class UpdateUserView(SuccessMessageMixin, LoginRequiredMixin, edit.UpdateView):
    model = CustomUser
    form_class = UserCreationForm
    template_name = "cuser_app/update_user.html"
    success_url = reverse_lazy('home')
    success_message = "Se han actualizado los datos del usuario %(email)s"


#DeleteView:
class DeleteUserView(SuccessMessageMixin, LoginRequiredMixin, edit.DeleteView):
    model = CustomUser
    template_name= "cuser_app/delete_user.html"
    success_url = reverse_lazy('home')
    success_message = "Se han borrado el usuario"
