from datetime import date
import pytest
from src.config import WEATHER_FIELDS
from src.services.runtime import build_application
from src.services.presentation import filter_period, chart_frame
from src.components.charts import weather_chart


def test_period_is_inclusive_and_does_not_mutate():
    frame = build_application().frame
    subset = filter_period(frame,date(2026,11,1),date(2026,11,1))
    assert len(subset) == 24
    assert len(frame) == 166
    assert subset.timestamp.dt.date.eq(date(2026,11,1)).all()


def test_empty_period_and_kind_filters():
    frame = build_application().frame
    assert filter_period(frame,date(2027,1,1),date(2027,1,2)).empty
    assert filter_period(frame,date(2026,11,1),date(2026,11,7),["forecast"]).empty
    assert filter_period(frame,date(2026,11,1),date(2026,11,7),[]).empty
    with pytest.raises(ValueError): filter_period(frame,date(2026,11,7),date(2026,11,1))


@pytest.mark.parametrize("field", list(WEATHER_FIELDS))
def test_charts_have_units_and_all_rows(field):
    frame = build_application().frame
    prepared = chart_frame(frame,field)
    assert len(prepared) == len(frame)
    assert prepared.timestamp.is_monotonic_increasing
    fig = weather_chart(frame,field)
    assert WEATHER_FIELDS[field][1] in fig.layout.yaxis.title.text
    assert len(fig.data) == 1
    if field != "precipitation_mm": assert fig.data[0].connectgaps is False


def test_missing_values_not_filled_for_charts():
    data = build_application().frame
    assert chart_frame(data,"temperature_c").temperature_c.isna().sum() == 2
