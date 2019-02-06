from operator import itemgetter

from repose.ts import thin_time_sequence


def generate_chart_data(db, resolution=None):
    hashes_and_times = db.get_hashes_and_times()
    if resolution:
        hashes_and_times = thin_time_sequence(
            hashes_and_times,
            time_getter=itemgetter(1),
            interval=resolution,
        )

    for hash, time in hashes_and_times:
        data = db.get_data(hash)
        by_language = {language: info['code'] for (language, info) in data.items()}
        for language, num in by_language.items():
            yield {'language': language, 'count': num, 'date': time.isoformat(' ')}


def generate_streamchart(chart_data):
    import altair as alt
    chart_data = list(chart_data)
    data = alt.Data(values=chart_data)

    chart = alt.Chart(data, width=1200, height=800).mark_area().encode(
        alt.X(
            field='date',
            type='temporal',
            axis=alt.Axis(format='%Y-%m-%d', domain=False, tickSize=0),
        ),
        alt.Y(
            field='count',
            aggregate='sum',
            type='quantitative',
            stack='zero',
            axis=alt.Axis(title='LOC'),
        ),
        alt.Color(
            field='language',
            type='nominal',
            scale=alt.Scale(scheme='category20b'),
        )
    )
    return chart
