import base64
import hashlib
import hmac
import os
import sys

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from requests.packages.urllib3.util import parse_url

from .forms import NewTopicForm
from .ml import predict
from .models import Board, Post, Topic

# Create your views here.


@csrf_exempt
def upload(request):
   
    if request.method == 'POST' and request.FILES['file']:
        
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        prediction = predict(filename)

        return JsonResponse({'image':str(uploaded_file_url), 'prediction': prediction})

def getimage(request):
    if request.method == 'GET':
        
        imgUrl = str(GetIMageFromCoordinate(request.GET['latitude'],request.GET['longitude']))
        filename = getImage(imgUrl)
        prediction = predict(filename)
        return JsonResponse({'imageUrl':imgUrl, 'prediction': prediction})
     


def sign_url(input_url=None, key=None, client_secret=None):
  """ Sign a request URL with a Crypto Key.
      Usage:
      from urlsigner import sign_url
      signed_url = sign_url(input_url=my_url,
                            key=key,
                            client_secret=CLIENT_SECRET)
      Args:
      input_url - The URL to sign
      key - Your Client ID
      client_secret - Your Crypto Key
      Returns:
      The signed request URL
  """
  # Return if any parameters aren't given
  if not input_url or not key or not client_secret:
    return None

  # Add the Client ID to the URL
  input_url += "&key=%s" % (key)

  url = parse_url(input_url)

  # We only need to sign the path+query part of the string
  url_to_sign = url.path + "?" + url.query

  # Decode the private key into its binary format
  # We need to decode the URL-encoded private key
  decoded_key = base64.urlsafe_b64decode(client_secret)

  # Create a signature using the private key and the URL-encoded
  # string using HMAC SHA1. This signature will be binary.
  signature = hmac.new(decoded_key, url_to_sign.encode(), hashlib.sha1)

  # Encode the binary signature into base64 for use within a URL
  encoded_signature = base64.urlsafe_b64encode(signature.digest())

  original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

  # Return signed URL
  return original_url + "&signature=" + encoded_signature.decode()
############################################
  

def getImage(url):
    try:        
            response = requests.get(url)
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

    filename = os.path.join(settings.MEDIA_ROOT, 'upload.png')
    with open(filename, 'wb') as f:
            f.write(response.content)

    return filename

def GetIMageFromCoordinate(lat,long): 
    
    url = sign_url('https://maps.googleapis.com/maps/api/staticmap?center='+str(lat)+','+str(long)+'&zoom=13&size=622x656&maptype=satellite&sensor=false&scale=1','AIzaSyDW6cuT1zime0ZKVjjiPdytH0Zw3Lu-zng','csXUTpXVywdChe162O39li2jKAM=')
    return getImage(url)
    
def home(request):
    return render(request, 'index.html', {'boards': Board.objects.all()})


def board_topics(request, boardid):
    board = get_object_or_404(Board, id=boardid)

    return render(request, 'topics.html', {'board': board})


def new_topic(request, boardid):
    board = get_object_or_404(Board, id=boardid)

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        user = User.objects.first()  # TODO: get the currently logged in user
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.creator = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                creator=user
            )
            # TODO: redirect to the created topic page
            return redirect('board_topics', boardid=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
