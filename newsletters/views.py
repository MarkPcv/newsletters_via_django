from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from newsletters.forms import ClientForm, NewsletterForm, ContentForm
from newsletters.models import Client, Newsletter, Content, Trial


def index(request):
    # Testing
    return render(request, 'newsletters/base.html')


class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletters:client_list')

    # Basic validation using models fields
    def form_valid(self, form):
        return super().form_valid(form)


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('newsletters:client_update', args=[self.object.pk])

    # Basic validation using models fields
    def form_valid(self, form):
        return super().form_valid(form)


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('newsletters:client_list')


class NewsletterListView(ListView):
    model = Newsletter

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        # Get information of newsletter content
        context_data['content_list'] = Content.objects.all()
        return context_data


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletters:newsletter_list')

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
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class NewsletterDetailView(DetailView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Retrieve content for newsletter
        content_item = Content.objects.get(settings=self.object)
        context_data['content'] = content_item
        # Retrieve last trial for newsletter
        try:
            # trial = Trial.objects.get(pk=self.kwargs.get('pk'))
            trial = Trial.objects.all()
            print(trial.last())
            if trial:
                context_data['trial'] = trial.last()
        except Trial.DoesNotExist:
            pass
        return context_data


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm

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


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletters:newsletter_list')

    #Get title for newsletter
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Retrieve content for newsletter
        content_item = Content.objects.get(settings=self.object)
        print(content_item.title)
        context_data['title'] = content_item.title
        return context_data


class TrialListView(ListView):
    model = Trial

    # Get all trials for specific newsletter
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            content_id=self.kwargs.get('pk'),
        )
        return queryset

