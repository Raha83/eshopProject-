from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .forms import ContactUsModelForm
from .models import UserProfile
from site_module.models import SiteSetting 

# Create your views here.

class ContactUsView(CreateView):
    template_name='contact_module/contact_us_page.html'
    form_class=ContactUsModelForm
    success_url='/'

    def get_context_data(self,*args,**kwargs):
        context= super().get_context_data(*args,**kwargs)
        site_setting : SiteSetting=SiteSetting.objects.filter(is_main_setting=True).first()
        
        context['site_setting']=site_setting
        return context
    
    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)

    # def post(self,request):
    #     contact_form=ContactUsModelForm(request.POST)
    #     if contact_form.is_valid():
    #         contact_form.save()
    #         return redirect("home_page")
    #     return render(request,'contact_module/contact_us_page.html',{
    #              "contact_form":contact_form
    #     })
        
def contact_us_page(request):
    # if request.method == "POST":
    #     entered_email=request.POST["email"]
    #     if entered_email=="":
    #         return render(request,'contact_module/contact_us_page.html',{
    #             "has_error":True
    #         })
    #     print(request.POST["name"]) 
    #     print(request.POST["email"])
    #     print(request.POST["subject"])
    #     print(request.POST["message"])
    #     return redirect(reverse("home_page"))
    if request.method == "POST":
        # contact_form=ContactUsForm(request.POST)
        contact_form=ContactUsModelForm(request.POST)
        if contact_form.is_valid():
            # print(contact_form.cleaned_data)
            # contact=ContactUs(
            #     title=contact_form.cleaned_data.get("title"),
            #     full_name=contact_form.cleaned_data.get("full_name"),
            #     email=contact_form.cleaned_data.get("email"),
            #     message=contact_form.cleaned_data.get("message")
            # )
            # contact.save()
            contact_form.save()
            return redirect("home_page")
    else:
        # contact_form=ContactUsForm()
        contact_form=ContactUsModelForm()
    return render(request,'contact_module/contact_us_page.html',{
                 "contact_form":contact_form
    })

def store_file(file):
    with open('temp/image.jpg' , 'wb+')as dest:
        for chunk in file.chunks():
            dest.write(chunk)

class CreateProfileView(CreateView):
    template_name="contact_module/create_profile_page.html"
    model=UserProfile
    fields='__all__'
    success_url='/'
    # def get(self,request):
    #     form=ProfileForm()
    #     return render(request,'contact_module/create_profile_page.html',context={
    #         'form':form
    #     })
    # def post(self,request):
    #     submitted_form=ProfileForm(request.POST,request.FILES )
    #     if submitted_form.is_valid():
    #         # store_file(request.FILES['user_image'])
    #         profile=UserProfile(image=request.FILES['user_image'])
    #         profile.save()
    #         return redirect('/')
    #     return render(request,'contact_module/create_profile_page.html',context={
    #         'form':submitted_form
    #     })

class ProfilesView(ListView):
    template_name='contact_module/profile_list_page.html'
    model=UserProfile
    context_object_name='profiles'