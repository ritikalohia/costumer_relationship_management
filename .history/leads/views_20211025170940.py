from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse 
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
from django.http import HttpResponse
from django.views import generic 
from .models import Lead, Agent, Category
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")


#CRUD+L - Create, Retrieve, Update and Delete + List
class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

# Create your views here.
def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    #queryset = Lead.objects.all()
    context_object_name = "leads"

    def get_queryset(self):  
        user = self.request.user

        #initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            #filter for the agent that is logged in 
            queryset = queryset.filter(agent__user=user)
        return queryset    

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context


def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads" :  leads
    }
    return render(request, "leads/lead_list.html", context)



class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

    def get_queryset(self):  
        user = self.request.user

        #initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            #filter for the agent that is logged in 
            queryset = queryset.filter(agent__user=user)
        return queryset 

def lead_details(request, pk):
    lead = Lead.objects.get(id=pk)
    context={
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        #TODO send email
        send_mail(
            subject=" A lead has been created", 
            message="Go to the site to see the new lead",
            from_email= "test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)



def lead_create(request):
    form = LeadModelForm()
    if request.method=="POST":
        form = LeadModelForm(request.POST)  
        if form.is_valid():
            form.save()       
            return redirect("/leads")
    context={
        "form": form
    }
    return render(request, "leads/lead_create.html", context)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    def get_queryset(self):  
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method=="POST":
        form = LeadModelForm(request.POST)  
        if form.is_valid():
            form.save()       
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)


class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):  
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")


class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent =form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent =agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"
    
    # def get_context_data(self, **kwargs):
    #     context = super(CategoryListView, self).get_context_data(**kwargs)
    #     user = self.request.user

    #     if user.is_organisor:
    #         queryset = Category.objects.filter(organisation=user.userprofile)
    #     else:
    #         queryset = Category.objects.filter(organisation=user.agent.organisation)

    #     context.update({
    #         "unassigned_lead_count": queryset.filter(category__isnull=True).count()
    #     })
    #     return context

    def get_queryset(self):  
        user = self.request.user
        #initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "cat"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     #qs = Lead.objects.filter(category=self.get_object())
    #     leads = self.get_object().leads.all()

    #     context.update({
    #         "leads": leads
    #     })
    #     return context


    def get_queryset(self):  
        user = self.request.user

        #initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset









