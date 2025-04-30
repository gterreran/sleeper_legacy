from stats.models import UserProfile, SleeperUser

def shared_context(request):
    user = request.user
    common_data = {
        "user": user,
    }

    # Add data based on the request if needed
    if user.is_authenticated:
        common_data["profile"] = UserProfile.objects.get(user = user)
        common_data["sleeper_users"] = SleeperUser.objects.filter(user = common_data["profile"])

    return common_data
