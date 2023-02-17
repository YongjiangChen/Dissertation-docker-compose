from typing import Any

from django_echarts.entities import (
    Container, RowContainer, ValuesPanel, Title, ElementEntity
)
from django_echarts.stores.entity_factory import factory
from django_echarts.views import PageTemplateView



class MyDashboardView(PageTemplateView):
    template_name = 'dashboard.html'

    
    def get_container_obj(self) -> Any:
        container = Container(div_class='container-fluid')
        mrc = RowContainer()
        container.add_widget(mrc)
        rc1 = RowContainer()

        mrc.add_widget(rc1)

        number_p = ValuesPanel()
        number_p.add('89.00', 'ClosePrice', 'USD', catalog='danger')
        rc1.add_widget(number_p)

        rc2 = RowContainer()
        ee2 = ElementEntity('img', id_='stock_price_predictions', width="200%", src="/static/stock_price_predictions.jpg")
        ##<img id="myimg" height="200px" src="/static/stock_price_predictions.jpg"/>
        rc2.add_widget(ee2)

        mrc.add_widget(rc2)

        rc3 = RowContainer()
        mrc.add_widget(rc3)
        return container