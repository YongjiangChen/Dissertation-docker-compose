from typing import Any

from django_echarts.entities import (
    Container, RowContainer, ValuesPanel, Title
)
from django_echarts.stores.entity_factory import factory
from django_echarts.views import PageTemplateView


class MyDashboardView2(PageTemplateView):
    template_name = 'dashboard.html'

    def get_container_obj(self) -> Any:
        container = Container(div_class='container-fluid')
        mrc = RowContainer()
        container.add_widget(mrc)
        rc1 = RowContainer()

        mrc.add_widget(rc1)

        number_p = ValuesPanel()
        number_p.add('89.00', 'ClosePrice', 'USD', catalog='success')
        rc1.add_widget(number_p, span=12)

        rc2 = RowContainer()
        rc2.add_widget(factory.get_widget_by_name('get_tu'), height='600px')

        mrc.add_widget(rc2)

        rc3 = RowContainer()
        mrc.add_widget(rc3)
        return container