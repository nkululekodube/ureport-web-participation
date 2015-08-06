from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# @login_required
def poll(request, poll_id):

    if request.method == 'GET':
        return render(request, 'poll.html', {'poll_id': poll_id})
