from apps.schedule.models import Schedule


def schedule_context_processor(request):
    try:
        current_user = request.session['login_info'].get('id')
        if current_user:
            mysked = Schedule.objects.filter(user=current_user)[:3:-1]
            context = {
                'mysked': mysked,
            }
            return context
    except KeyError as e:
        mysked = Schedule.objects.all()
        context = {
            'mysked': mysked,
        }
        return context
    except Exception as e:
        print(e)
