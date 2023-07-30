from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from newsletters.forms import ClientForm, NewsletterForm, ContentForm
from newsletters.models import Client, Newsletter, Content, Trial

## TODO: Implement main page
def index(request):
    # Testing
    return render(request, 'newsletters/base.html')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    # Display only user's clients
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletters:client_list')
    permission_required = 'newsletters.add_client'

    # Basic validation using models fields
    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)




class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = 'newsletters.view_client'


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'newsletters.change_client'

    def get_success_url(self):
        return reverse('newsletters:client_update', args=[self.object.pk])

    # Basic validation using models fields
    def form_valid(self, form):
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('newsletters:client_list')
    permission_required = 'newsletters.delete_client'


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter

    # Display only user's newsletters
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        # Get information of newsletter content
        context_data['content_list'] = Content.objects.all()
        return context_data


class NewsletterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletters:newsletter_list')
    permission_required = 'newsletters.add_newsletter'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ContentFormSet = inlineformset_factory(Newsletter, Content, form=ContentForm, extra=1, can_delete=False)
        if self.request.method == 'POST':
            formset = ContentFormSet(self.request.POST, instance=self.object)
        else:
            formset = ContentFormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        self.object.status = 'created'
        self.object.owner = self.request.user
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class NewsletterDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Newsletter
    permission_required = 'newsletters.view_newsletter'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Retrieve content for newsletter
        content_item = Content.objects.get(settings=self.object)
        context_data['content'] = content_item
        # Retrieve last trial for newsletter
        # try:
        #     trial = Trial.objects.all()
        #     if trial:
        #         context_data['trial'] = trial.last()
        # except Trial.DoesNotExist:
        #     pass
        return context_data


class NewsletterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    permission_required = 'newsletters.change_newsletter'

    # Prevent editing to newsletter of another user
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('newsletters:newsletter_update', args=[self.object.pk])

    # Basic validation using models fields
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ContentFormSet = inlineformset_factory(Newsletter, Content, form=ContentForm, extra=0, can_delete=False)
        if self.request.method == 'POST':
            formset = ContentFormSet(self.request.POST, instance=self.object)
        else:
            formset = ContentFormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        self.object.status = 'created'
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class NewsletterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletters:newsletter_list')
    permission_required = 'newsletters.delete_newsletter'

    #Get title for newsletter
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Retrieve content for newsletter
        content_item = Content.objects.get(settings=self.object)
        print(content_item.title)
        context_data['title'] = content_item.title
        return context_data


class TrialListView(LoginRequiredMixin, ListView):
    model = Trial

    # Get all trials for specific newsletter
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            content_id=self.kwargs.get('pk'),
        )
        return queryset

