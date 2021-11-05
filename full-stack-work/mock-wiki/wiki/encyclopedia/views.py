from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random

from . import util

"""
On left bar, there is ability to search, home, create a new page
or return a random one.

A page will be opened using the subject method.

When one opens a specific or random page, they have the ability to
edit that page using the editpage method.
"""

INVALID = "invalid request"
DUPLICATE = "duplicate file"


def searchpage(request):
    if request.method == "POST":
        if "q" in request.POST:
            title = request.POST["q"]
            entry = util.get_entry(title)

            if entry:
                return HttpResponseRedirect(reverse("subject", args=(title,)))

            possible_entries = []
            for entry in util.list_entries():
                if title.lower() in entry.lower():
                    possible_entries.append(entry)

            return render(request, "encyclopedia/searchpage.html", {
                "q": title,
                "entries": possible_entries
            })

        return render(request, "encyclopedia/error.html", {
            "error": INVALID  # if not containing "q"
        })

    return render(request, "encyclopedia/index.html")  # if not POST


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def newpage(request):
    if request.method == "POST":
        if "title" in request.POST and "content" in request.POST:
            title = request.POST["title"]
            content = request.POST["content"]

            for entry in util.list_entries():
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/error.html", {
                        "error": DUPLICATE  # if exists
                    })

            util.save_entry(title, content)  # if saved redirect
            return HttpResponseRedirect(reverse("subject", args=(title, )))

        return render(request, "encyclopedia/error.html", {
            "error": INVALID  # if doesn't have content
        })

    return render(request, "encyclopedia/newpage.html")  # if nothing posted


def randompage(request):
    entries = util.list_entries()
    title = random.choice(entries)  # get a random entry without edit capacity
    content = util.convert_to_html(title)  # get correct html
    return render(request, "encyclopedia/randompage.html", {
        "content": content
    })


def subject(request, title):
    if title not in util.list_entries():  # wrong subject
        return HttpResponse(f"Your requested page, {title}, was not found.")
    content = util.convert_to_html(title)  # get correct html
    return render(request, f"encyclopedia/subject.html", {
        "title": title,
        "content": content
    })


def editpage(request):
    if request.method == "POST":
        if "title" in request.POST and "content" in request.POST:
            title = request.POST["title"]
            content = request.POST["content"]

            util.save_entry(title, content)  # if saved redirect
            return HttpResponseRedirect(reverse("subject", args=(title, )))

        return render(request, "encyclopedia/error.html", {
            "error": INVALID  # if doesn't have content
        })
    elif request.method == "GET":
        if "title" in request.GET:
            title = request.GET["title"]
            content = util.get_entry(title)
            return render(request, "encyclopedia/editpage.html", {
                "content": content,
                "title": title
            })
        return render(request, "encyclopedia/error.html", {
            "error": INVALID
        })
