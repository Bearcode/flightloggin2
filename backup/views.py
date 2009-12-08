import datetime

from share.decorator import no_share, secret_key
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from annoying.decorators import render_to

from classes import Backup, EmailBackup


@login_required()   
def backup(request, shared, display_user):
    
    # get a zip file of the csv of the users data
    sio = Backup(display_user).output_zip()
    
    DATE = datetime.date.today()
    
    response = HttpResponse(sio.getvalue(), mimetype='application/zip')
    response['Content-Disposition'] = \
                'attachment; filename=logbook-backup-%s.tsv.zip' % DATE

    return response

#################################
#################################
#################################

@no_share('NEVER')
@login_required
def emailbackup(request, shared, display_user):
    """Send email backup to the user"""
    
    email = EmailBackup(display_user)
    sent = email.send()
    
    return HttpResponse("email sent to %s" % sent, mimetype='text-plain')

@secret_key
def schedule(request, schedule):
    """Only send out the emails to the people who's schedule is exactly the
       one being passed as 'schedule'
    """
    
    from django.contrib.auth.models import User
    if schedule == 'weekly':
        users = User.objects.filter(profile__backup_freq=1)
    
    elif schedule == 'biweekly':
        users = User.objects.filter(profile__backup_freq=2)
    
    elif schedule == 'monthly':
        users = User.objects.filter(profile__backup_freq=3)
    
    ret = "%s - %s " % (schedule, datetime.datetime.now())    
    for user in users:
        em = EmailBackup(user, auto=True)
        result = em.send(test=True)
        ret += "%s [%s]\n" % (user.username, result)
    
    
    return HttpResponse(ret, mimetype="text/plain")

##
## crontab:
##
#30 5 1         * * wget http://flightlogg.in/schedule-monthly.py?sk=
#30 4 1,7,14,21 * * wget http://flightlogg.in/schedule-weekly.py?sk=
#30 3 1,14      * * wget http://flightlogg.in/schedule-biweekly.py?sk=
