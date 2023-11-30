from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            group, created = Group.objects.get_or_create(name='RegularUserGroup')
            user.groups.add(group)

            return redirect('admin/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
