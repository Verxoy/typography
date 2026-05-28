"""Редирект /staff/… с Django (порт API) на фронтенд Vue."""
from __future__ import annotations

from django.http import HttpResponseRedirect
from django.views import View

from .models_quotes import QuoteRequest
from .quote_links import frontend_base_url, staff_quote_detail_url
from .quote_resolve import get_quote_by_ref


class StaffQuoteListRedirectView(View):
    def get(self, request):
        return HttpResponseRedirect(f'{frontend_base_url()}/staff/quotes')


class StaffQuoteDetailRedirectView(View):
    def get(self, request, ref: str):
        try:
            quote = get_quote_by_ref(ref)
        except QuoteRequest.DoesNotExist:
            return HttpResponseRedirect(f'{frontend_base_url()}/staff/quotes')
        return HttpResponseRedirect(staff_quote_detail_url(quote))


class StaffLoginRedirectView(View):
    def get(self, request):
        redirect_to = request.GET.get('redirect', '')
        url = f'{frontend_base_url()}/staff/login'
        if redirect_to and redirect_to.startswith('/staff/'):
            from urllib.parse import urlencode

            url = f'{url}?{urlencode({"redirect": redirect_to})}'
        return HttpResponseRedirect(url)
