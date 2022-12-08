from django.views.generic import ListView
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
            queryset = queryset.filter(self.get_query()) # filter(Q()) == all()
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

# class CreateView(View):
#     form_class = None
#     template_name = None
#     model = None
#     redirect_url = None
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         context = {'form': form}
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(data=request.POST)
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         self.object = form.save()
#         return redirect(self.get_redirect_url())
#
#     def form_invalid(self, form):
#         context = {'form': form}
#         return render(self.request, self.template_name, context)
#
#     def get_redirect_url(self):
#         return self.redirect_url
#
#
#
# class DetailView(TemplateView):
#     context_key = 'object'
#     model = None
#     key_kwarg = 'pk'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context[self.context_key] = self.get_object()
#         return context
#
#     def get_object(self):
#         pk = self.kwargs.get(self.key_kwarg)
#         return get_object_or_404(self.model, pk=pk)
#
#
# class ListView(TemplateView):
#     model = None
#     context_key = 'objects'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context[self.context_key] = self.get_objects()
#         return context
#
#     def get_objects(self):
#         return self.model.objects.all()
#
#
# class FormView(View):
#     template_name = None
#     form_class = None
#     redirect_url = ''
#
#     def get_context_data(self, **kwargs):
#         return kwargs
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         context = self.get_context_data(form=form)
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(data=request.POST)
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def get_redirect_url(self):
#         return self.redirect_url
#
#     def form_valid(self, form):
#         return redirect(self.get_redirect_url())
#
#     def form_invalid(self, form):
#         context = self.get_context_data(form=form)
#         return render(self.request, self.template_name, context)