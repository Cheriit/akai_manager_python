from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .forms import MeetingCreateForm, MeetingsRegisterForm
from .models import Meeting
from django.contrib import messages
from django.views.generic import (
    DetailView,
    ListView)


@staff_member_required
def create(request):
    if request.method == 'POST':
        form = MeetingCreateForm(request.POST)

        if form.is_valid():
            meeting = form.save()
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            messages.success(request, f'Spotkanie {date} o godzinie {time} zostało utworzone pomyślnie!')
            return redirect('meeting_view', pk=meeting.pk)
    else:
        form = MeetingCreateForm()
    return render(request, 'meetings/meeting_create.html', {'form': form})


def register(request, **kwargs):
    form = MeetingsRegisterForm(request.POST or None)
    if request.method == 'GET':
        if Meeting.objects.filter(is_active=True, **kwargs).exists() and 'code' in kwargs:
            meeting = Meeting.objects.get(is_active=True, **kwargs)
            if not Meeting.objects.filter(members=request.user, pk=meeting.pk).exists():
                meeting.members.add(request.user)
                meeting.save()
                messages.success(request, f'Spotkanie {meeting.date} o godzinie {meeting.time} zanotowało obecność {request.user}!')
                return redirect('meeting_view', pk=meeting.pk)
            else:
                return redirect('meeting_view', pk=meeting.pk)
        else:
            return render(request, 'meetings/meeting_register.html', {'form': form})
    elif request.method == 'POST':
        if Meeting.objects.filter(is_active=True, code=form.data['code']).exists():
            meeting = Meeting.objects.get(is_active=True, code=form.data['code'])
            if not Meeting.objects.filter(members=request.user, pk=meeting.pk).exists():
                if form.is_valid():
                    meeting.members.add(request.user)
                    meeting.save()
                    messages.success(request, f'Spotkanie {meeting.date} o godzinie {meeting.time} zanotowało obecność {request.user}!')
                    return redirect('meeting_view', pk=meeting.pk)
            else:
                return redirect('meeting_view', pk=meeting.pk)
        else:
            return render(request, 'meetings/meeting_register.html', {'form': form})


class MeetingDetailView(LoginRequiredMixin, DetailView):
    model = Meeting


class MeetingListView(LoginRequiredMixin, ListView):
    model = Meeting
    ordering = ['-date', '-time']
