from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, render_to_response,redirect
import sys
import re
import urllib.parse
import html.parser

from .forms import CheckURL


def index(request):
    url_check = CheckURL(request.POST or None)
    context = {
        "title": "Get URL",
        "content": "Page to get URL",
        "form": url_check
    }

    return render(request, "check/home.html", context)


def test(request):

    a = request.POST.get('url')

    # print("URL is ", a)
    # if url_check.is_valid():
    #     print(url_check.cleaned_data)
    # # if request.method == 'POST':
    # #     print(request.POST)
    # #     print(request.POST.get('url'))

    rewrittenurl = str(a)
    print(rewrittenurl)
    match = re.search(r'https://urldefense.proofpoint.com/(v[0-9])/', rewrittenurl)
    if match:
        if match.group(1) == 'v1':
            match = re.search(r'u=(.+?)&k=', rewrittenurl)
            if match:
                urlencodedurl = match.group(1)
                htmlencodedurl = urllib.parse.unquote(urlencodedurl)
                url = html.parser.HTMLParser().unescape(htmlencodedurl)
                context = {
                    'url_': url
                }
                print(url)
                return render(request, 'check/result.html', context)
            else:
                print('Error parsing URL')
        elif match.group(1) == 'v2':
            match = re.search(r'u=(.+?)&[dc]=', rewrittenurl)

            if match:

                specialencodedurl = match.group(1)
                trans = str.maketrans('-_', '%/')
                urlencodedurl = specialencodedurl.translate(trans)
                htmlencodedurl = urllib.parse.unquote(urlencodedurl)
                url = html.parser.HTMLParser().unescape(htmlencodedurl)
                context = {
                    'input_url': rewrittenurl,
                    'url_': url
                }
                print("DECODED URL:", context)
                return render(request, 'check/result.html', context)

            else:
                print('Error parsing URL')
        else:
            print('Unrecognized version in: ', rewrittenurl)

    else:
        print('No valid URL found in input: ', rewrittenurl)






