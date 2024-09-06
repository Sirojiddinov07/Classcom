import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def change_language(request):
    if request.method == "POST":
        data = json.loads(request.body)
        language_code = data.get("language_code")
        if language_code:
            request.session[settings.LANGUAGE_COOKIE_NAME] = language_code
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)
