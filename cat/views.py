from django.shortcuts import redirect, render

from .cat import Cat


SESSION_CAT_KEY = 'cat'


def index(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            request.session[SESSION_CAT_KEY] = Cat(name=name).to_session()
            return redirect('cat_info')

    return render(request, 'cat/index.html')


def cat_info(request):
    cat_data = request.session.get(SESSION_CAT_KEY)
    if not cat_data:
        return redirect('index')

    cat = Cat.from_session(cat_data)

    if request.method == 'POST':
        cat.apply_action(request.POST.get('action'))
        request.session[SESSION_CAT_KEY] = cat.to_session()
        return redirect('cat_info')

    return render(request, 'cat/cat_info.html', {'cat': cat})
