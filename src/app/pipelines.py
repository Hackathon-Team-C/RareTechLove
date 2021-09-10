from django.contrib.auth.models import User
from django_slack_oauth.models import SlackUser


def register_user(request, api_data):
    if api_data['ok']:
        user, created = User.objects.get_or_create(
            username=api_data['team_id']+':'+api_data['user_id']
        )

        if user.is_active:
            slacker, _ = SlackUser.objects.get_or_create(slacker=user)
            slacker.access_token = api_data.pop('access_token')
            slacker.extras = api_data
            slacker.save()

        if created:
            request.created_user = user

    return request, api_data

def notify(request, api_data):
    if hasattr(request, 'created_user'):
        notify_admins("New user with id {} has been created.".format(request.created_user))
        notify_user(request.created_user)

    return request, api_data

def debug_oauth_request(request, api_data):
    print(api_data)
    return request, api_data

