import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def convert_to_html(title):
    """
    Returns content from md file as html content in a string called content.
    Gets safe escaped from HTML template.
    """
    entry = get_entry(title)

    entry = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", entry)
    entry = re.sub(r"\[(.*?)\]\((.*?)\)", r"<a href='\2'>\1</strong>", entry)

    content = ""
    lines = entry.splitlines()
    result = ""
    heading = re.compile('#{1,6}')
    insideList = False

    for line in lines:
        result = ""

        isHeading = heading.match(line)  # bool if heading

        if line.startswith("* "):
            if not insideList:
                result += "<ul> \n"
                insideList = True  # we are inside the list.
            result += ("<li>" + line[2:] + "</li>")
        else:
            if insideList:
                result += "</ul> \n"
                insideList = False  # no longer inside list.
            if isHeading:
                headingNum = isHeading.span()[1]  # 1-6
                result = re.sub("#{1,6} (.*)",
                                f"<h{headingNum}> {line[headingNum+1:]} \
                                </h{headingNum}>", line)
            else:
                result += "<p>" + line + "</p>"

        content += result + "\n"
    return content
