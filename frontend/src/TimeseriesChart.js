import React, { Component } from 'react';

import ReactHighcharts from 'react-highcharts';
import highchartsMore from 'highcharts-more';

export default class App extends Component {

    componentWillMount() {
        highchartsMore(ReactHighcharts.Highcharts);
    }

    render() {
        const config = {
            tooltip: { enabled: false },
            chart: {
                renderTo: 'container',
            },
            title: {
                text: 'Data Quality'
            },
            subtitle: {
                text: 'Red zones are ones where the data regarding the sensors is suspected of having low quality'
            },
            xAxis: {
                type: 'Time'
            },
            yAxis: {
                title: {
                    text: 'Amps'
                },
                min: 0,
                max: 1
            },
            legend: {
                enabled: false
            },

            plotOptions: {
                series: {
                    fillColor: 'transparent'
                },
                line: {
                    animation: false
                },
                turboThreshold: 10,
            },

            series: [
                {
                    name: 'Values',
                    data: this.props.blueLine,
                    color: 'blue',
                    lineWidth: 0.5,
                    enableMouseTracking: false,
                    marker: {
                        enabled: false,
                    }
                },
                {
                    name: 'Values',
                    data: this.props.redDots,
                    color: 'red',
                    lineWidth: 0,
                    marker: {
                        radius: 1,
                    },
                    enableMouseTracking: false,
                },

            ]
        };

        return (
            <div>
                <ReactHighcharts config={config} ref="chart" />
            </div>
        );
    }
}
