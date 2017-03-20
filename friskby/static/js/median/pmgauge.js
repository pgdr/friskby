function pmgauge(value_pm25, value_pm10) {
    console.log("making gauge");
    console.log("with val " + value_pm25);
    console.log("with val " + value_pm10);
    var gaugeOptions = {
        chart: {
            type: 'solidgauge'
        },

        title: null,

        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },

        tooltip: {
            enabled: false
        },

        // the value axis
        yAxis: {
            stops: [
                [0.1, '#55BF3B'], // green
                [0.3, '#DDDF0D'], // yellow
                [0.4, '#DF5353'], // red
                [0.6, '#871F78'], // purple
                [0.8, '#000000']  // black
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickAmount: 2,
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },

        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };

    // The PM25 gauge
    var chartPM25 = Highcharts.chart('container-PM25', Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: 'PM25'
            }
        },

        credits: {
            enabled: false
        },

        series: [{
            name: 'PM25',
            data: [0],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                    '<span style="font-size:12px;color:silver">PM25&nbsp;&mu;g/m<sup>3</sup></span></div>'
            },
            tooltip: {
                valueSuffix: 'PM25&nbsp;&mu;g/m<sup>3</sup>'
            }
        }]
    }));

    // The PM10 gauge
    var chartPM10 = Highcharts.chart('container-PM10', Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: 'PM10'
            }
        },

        series: [{
            name: 'PM10',
            data: [0],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                    '<span style="font-size:12px;color:silver">PM10&nbsp;&mu;g/m<sup>3</sup></span></div>'
            },
            tooltip: {
                valueSuffix: 'PM10&nbsp;&mu;g/m<sup>3</sup>'
            }
        }]
    }));

    point = chartPM25.series[0].points[0];
    point.update(value_pm25);

    point = chartPM10.series[0].points[0];
    point.update(value_pm10);
}
