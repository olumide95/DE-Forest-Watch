import logging

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .utils import get_image_from_coordinate, predict

log = logging.getLogger(__name__)


@csrf_exempt
def upload(request):
    if request.method == "POST" and request.FILES["file"]:
        myfile = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        prediction = predict(filename)

        return JsonResponse({"image": str(uploaded_file_url), "prediction": prediction})

    return JsonResponse(
        {"success": False, "message": "Invalid request method. Please use POST."}
    )


def get_image(request):
    filename = get_image_from_coordinate(
        request.GET["latitude"], request.GET["longitude"]
    )
    prediction = predict(filename)

    return JsonResponse({"prediction": prediction})

    # try:
    #     filename = get_image_from_coordinate(
    #         request.GET["latitude"], request.GET["longitude"]
    #     )
    #     prediction = predict(filename)

    #     return JsonResponse({"prediction": prediction})
    # except Exception as e:
    #     log.exception(e)
    #     return JsonResponse(
    #         {
    #             "success": False,
    #             "message": "Bad request. Provide longitude and latitude.",
    #             "error": str(e),
    #         }
    #     )


def home(request):
    return JsonResponse({"success": True, "message": "Welcome to Forest Watch API!"})
