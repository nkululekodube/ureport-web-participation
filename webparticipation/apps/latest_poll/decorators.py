def show_untaken_latest_poll_message(view_func):
    def _decorated(request, *args, **kwargs):
        if request.GET.get('lp'):
            request.session.lp = True
        return view_func(request, *args, **kwargs)
    return _decorated
