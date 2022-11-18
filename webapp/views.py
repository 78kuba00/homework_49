from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from webapp.models import TrackerType, Tracker, TrackerStatus
from django.urls import reverse, reverse_lazy


class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        kwargs['tasks'] = Tracker.objects.all()
        return super().get_context_data(**kwargs)


class TaskView(TemplateView):
    template_name = 'task_view.html'
    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Tracker, pk=kwargs['task_pk'])
        return super().get_context_data(**kwargs)


class CreateView(View):
    def get(self, request, *args, **kwargs):
        context = {
           'statuses': TrackerStatus.objects.all(),
           'types': TrackerType.objects.all(),
        }
        return render(request, 'create.html', context)
    def post(self, request, *args, **kwargs):
        errors = {}
        summary = request.POST.get('summary')
        status = request.POST.get('status')
        type = request.POST.get('type')
        description = request.POST.get('description')
        if not summary:
            errors['summary'] = 'Краткое описание не можеть быть пустым'
        elif len('summary') > 200:
            errors['summary'] = 'Краткое описание не можеть быть длиннее 200 символов'
        elif len(description) > 3000:
            errors['description'] = 'Полное описание не можеть быть длиннее 3000 символов'
        new_task = Tracker.objects.create(summary=summary, status_id=status, description=description, type_id=type)
        return redirect('task_view', task_pk=new_task.pk)

class EditView(View):
    def get(self, request, pk):
        tracker = get_object_or_404(Tracker, pk=pk)
        context = {
            'summary': tracker.summary,
            'description': tracker.description,
            'statuses': TrackerStatus.objects.all(tracker.status.pk),
            'types': TrackerType.objects.all(tracker.type.pk)
        }
        return render(request, 'task_edit.html', context)
    def post(self, request, *args, **kwargs):
        # form = ProductForm(data=request.POST)
            summary = request.POST.get('summary')
            status = request.POST.get('status')
            type = request.POST.get('type')
            description = request.POST.get('description')
            edit_task = Tracker.objects.create(summary=summary, status_id=status, description=description, type_id=type)
        return redirect('task_view', task_pk=edit_task.pk)

class DeleteView(View):
   model = Tracker
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['tracker'] = self.object.tracker
       return context
def task_delete_view(request, pk):
    task = get_object_or_404(Tracker, pk=pk)
    if request.method =="GET":
        return render(request, 'task_delete.html', {'task': task})
    elif request.method =="POST":
        task.delete()
        return redirect('index')

    # task = get_object_or_404(Tracker, pk=pk)
    # if request.method == "GET":
    #     return render(request, 'task_edit.html', {'task': task, 'statuses': STATUS_CHOICES})
    # elif request.method == "POST":
    #     task.title = request.POST.get('title')
    #     task.status = request.POST.get('status')
    #     task.details = request.POST.get('details')
    #     task.deadline = request.POST.get('deadline')
    #     if not task.deadline:
    #         task.deadline = None
    #     task.save()
    #     return redirect('task_view', pk=task.pk)



