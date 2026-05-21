from django.shortcuts import redirect, render

from .models import Cat


SESSION_CAT_ID = 'cat_id'


def index(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            cat = Cat.objects.create(name=name)
            request.session[SESSION_CAT_ID] = cat.id
            return redirect('cat_info')

    return render(request, 'cat/index.html')


def cat_info(request):
    cat_id = request.session.get(SESSION_CAT_ID)
    if not cat_id:
        return redirect('index')

    try:
        cat = Cat.objects.get(id=cat_id)
    except Cat.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        cat.do_action(request.POST.get('action'))
        cat.save()
        return redirect('cat_info')

    return render(request, 'cat/cat_info.html', {'cat': cat})
