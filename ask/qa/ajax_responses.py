import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse


class HttpResponseAjax(HttpResponse):
    def __init__(self, status="ok", **kwargs):
        kwargs['status'] = status
        super(HttpResponseAjax, self).__init__(content=json.dump(kwargs),
                                               content_type="application/json")


class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super(HttpResponseAjaxError, self).__init__(status="Error", code=code, message=message)


def login_required_ajax(original_view):
    def new_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return original_view(request, *args, **kwargs)
        elif request.is_ajax():
            return HttpResponseAjaxError(code="no_auth", message="authorization required")
        else:
            HttpResponseRedirect(reverse('login') + "?continue=" + request.get_full_path())
    return new_view