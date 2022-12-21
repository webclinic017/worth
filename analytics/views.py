from datetime import datetime, date, timedelta

from plotly.offline import plot
import plotly.graph_objs as go

from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from analytics.cash import cash_sums, total_cash
from analytics.pnl import pnl_summary
from analytics.utils import total_realized_gains
from trades.ib_flex import get_trades
from moneycounter.dt import lbd_prior_month, our_now, lbd_of_month
from moneycounter.str_utils import is_near_zero
from worth.utils import df_to_jqtable
from markets.tbgyahoo import yahoo_url
from markets.models import Ticker
from trades.utils import weighted_average_price
from markets.utils import get_price, ticker_admin_url


class CheckingView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/checking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account_name = 'BofA'
        context['account'] = account_name
        balance, statement_balance = cash_sums(account_name)
        context['balance'] = balance
        context['statement_balance'] = statement_balance
        return context


class PnLView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getter = self.request.GET.get
        account = getter('account')
        days = getter('days')

        if days is not None:
            days = int(days)
            d = our_now() - timedelta(days=days)
            d = d.date()
        else:
            d = getter('d')

            if d is not None:
                try:
                    d = datetime.strptime(d, '%Y%m%d').date()
                except Exception:
                    n = 0
                    if d.isnumeric():
                        n = int(d)
                        d = our_now()
                        while n > 0:
                            d = lbd_prior_month(d)
                            n -= 1
            else:
                d = our_now().date()

        context['d'] = d
        context['headings1'], context['data1'], context['formats'], total_worth = \
            pnl_summary(d=d, a=account)
        context['title'] = 'PPM'
        return context


class TotalCashView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/total_cash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        getter = self.request.GET.get
        context['total_cash'] = total_cash()
        return context


class GetIBTradesView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headings1'], context['data1'], context['formats'] = get_trades()
        context['title'] = 'IB Futures Trades'
        return context


class TickerView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/ticker.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = Ticker.objects.get(ticker=context['ticker'])
        context['tickeradmin'] = ticker_admin_url(self.request, ticker)
        context['title'] = yahoo_url(ticker)
        context['description'] = ticker.description
        pos, wap = weighted_average_price(ticker)
        if is_near_zero(pos):
            context['msg'] = 'Zero position.'
        else:
            context['pos'] = pos
            context['open_price'] = wap

            try:
                price = get_price(ticker)
                context['price'] = price
                context['capital'] = pos * price
                context['pnl'] = ticker.market.cs * pos * (price - wap)
            except IndexError:
                context['msg'] = 'Could not get a price for this ticker.'

        return context


class ValueChartView(LoginRequiredMixin, TemplateView):
    title = 'Value Chart'
    template_name = 'analytics/value_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        getter = self.request.GET.get

        d = datetime.today().date()
        n_months = getter('n_months')
        if n_months is not None:
            x_axis = [d] + [d := lbd_prior_month(d) for i in range(int(n_months))]
            x_axis.reverse()
        else:
            y = d.year
            m = d.month
            x_axis = [lbd_of_month(date(y, i, 1)) for i in range(1, m)]
            x_axis.append(d)

        accnt = getter('accnt')

        y_axis = [pnl_summary(i, a=accnt)[-1] / 1.e6 for i in x_axis]
        x_axis = [f'{d:%Y-%m}' for d in x_axis]

        context['title'] = self.title

        fig = go.Figure(data=go.Scatter(x=x_axis, y=y_axis,
                        mode='lines', name='value',
                        opacity=0.8, marker_color='green'))
        fig.update_layout({'title_text': 'Value', 'yaxis_title': 'Millions($)'})

        context['plot_div'] = plot({'data': fig}, output_type='div')

        return context


class RealizedGainView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/table.html'

    def get_context_data(self, **kwargs):
        year = 2022
        realized, formatter = total_realized_gains(year)

        context = super().get_context_data(**kwargs)
        context['headings1'], context['data1'], context['formats'] = df_to_jqtable(df=realized, formatter=formatter)
        context['title'] = f'Realized Gains ({year})'
        return context
