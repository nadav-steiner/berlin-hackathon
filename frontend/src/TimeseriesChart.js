import React, { Component } from 'react';

import ReactHighcharts from 'react-highcharts';
import highchartsMore from 'highcharts-more';

export default class App extends Component {

    componentWillMount() {
        highchartsMore(ReactHighcharts.Highcharts);
    }

    render() {
        const redLineSeriesList = this.props.redLinesList;
        const nextRedLine = this.props.nextRedLine;
        let seriesList = [{
            name: 'Values',
            data: this.props.blueLine,
            color: 'blue',
            lineWidth: 0.5,
            enableMouseTracking: false,
            marker: {
                enabled: false,
            }}];
        seriesList = seriesList.concat(redLineSeriesList).concat(nextRedLine);

        console.log(this.props.blueLine[this.props.blueLine.length-1]);

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
                type: 'datetime',
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
                }
            },
            series: seriesList,
        };

        return (
            <div>
                <ReactHighcharts config={config} ref="chart" />
            </div>
        );
    }
}
