from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View
from django.db.models import Q
from django.utils.http import urlencode

class SearchView(ListView):
    search_form_class = None
    search_form_field = 'search'
    query_name = 'query'
    search_fields = []

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        if self.search_form_class:
            return self.search_form_class(self.request.GET)

    def get_search_value(self):
        if self.form:
            if self.form.is_valid():
                return self.form.cleaned_data[self.search_form_field]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(self.get_query())
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.form:
            context['form'] = self.form
            if self.search_value:
                context[self.query_name] = urlencode({self.search_form_field: self.search_value})
                context[self.search_form_field] = self.search_value
        return context

    def get_query(self):
        query = Q()
        for field in self.search_fields:
            kwargs = {field: self.search_value}
            query = query | Q(**kwargs)
        return query

class DeleteView(View):
    template_name = None
    confirm_deletion = True
    model = None
    key_kwarg = 'pk'
    context_key = 'object'
    redirect_url = ''

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.confirm_deletion:
            return render(request, self.template_name, self.get_context_data())
        else:
            self.perform_delete()
            return redirect(self.get_redirect_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.perform_delete()
        return redirect(self.get_redirect_url())

    def perform_delete(self):
        self.object.delete()

    def get_context_data(self, **kwargs):
        return {self.context_key: self.object}

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)

    def get_redirect_url(self):
        return self.redirect_url

class EditView(View):
   form_class = None
   template_name = None
   redirect_url = ''
   model = None
   key_kwarg = 'pk'
   context_key = 'object'

   def get(self, request, *args, **kwargs):
       self.object = self.get_object()
       form = self.form_class(instance=self.object)
       context = self.get_context_data(form=form)
       return render(request, self.template_name, context=context)

   def post(self, request, *args, **kwargs):
       self.object = self.get_object()
       form = self.form_class(instance=self.object, data=request.POST)
       if form.is_valid():
           return self.form_valid(form)
       else:
           return self.form_invalid(form)

   def form_valid(self, form):
       self.object = form.save()
       return redirect(self.get_redirect_url())

   def form_invalid(self, form):
       context = self.get_context_data(form=form)
       return render(self.request, self.template_name, context=context)

   def get_object(self):
       pk = self.kwargs.get(self.key_kwarg)
       return get_object_or_404(self.model, pk=pk)

   def get_context_data(self, **my_kwargs):
       context = self.kwargs.copy()
       context[self.context_key] = self.object
       context.update(my_kwargs)
       return context

   def get_redirect_url(self):
       return self.redirect_url