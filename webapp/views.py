from django.shortcuts import render, get_object_or_404
from django.views.generic import View,TemplateView
from webapp.models import TrackerType, Tracker, TrackerStatus


class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        kwargs['tasks'] = Tracker.objects.all()
        return super().get_context_data(**kwargs)

class TaskView(TemplateView):
    template_name = 'task_view.html'
    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Tracker,pk=kwargs['task_pk'])
        return super().get_context_data(**kwargs)
def task_view(request, pk):
    task = get_object_or_404(Tracker, pk=pk)
    context = {'task': task}
    return render(request, 'task_view.html', {'task': task})

# class IndexView(View):
#
#    def get(self, request, *args, **kwargs):
#        tasks = Tracker.objects.all()
#        context = {
#            'task': tasks
#        }
#        return render(request, 'index.html', context)
