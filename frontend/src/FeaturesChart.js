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
                text: 'Feature learning'
            },
            subtitle: {
                text: 'The line is the feature progression over time'
            },
            xAxis: {
                type: 'First Feature'
            },
            yAxis: {
                title: {
                    text: 'Second Feature'
                },
                // min: -1,
                // max: 1
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
            },

            series: [
                {
                    name: 'Values',
                    // data: [[1,0.1],[2,0.3],[3,0.2],[4,0.7],[5,0.1]],
                    data: this.props.featuresLine,
                    color: 'black',
                    lineWidth: 0.5,
                    enableMouseTracking: false,
                    marker: {
                        enabled: false,
                    }
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
