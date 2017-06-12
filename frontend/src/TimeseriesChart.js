import React, { Component } from 'react';
import ReactHighcharts from 'react-highcharts';
import highchartsMore from 'highcharts-more';

export default class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            values: this.props.values,
            highlightedArea: this.props.highlightedArea
        }
    }

    static componentWillMount() {
        highchartsMore(ReactHighcharts.Highcharts);
    }

    componentWillReceiveProps(nextProps) {

    }
    render() {
        const config = {
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
                    text: 'Wattage'
                }
            },
            legend: {
                enabled: false
            },

            plotOptions: {
                series: {
                    fillColor: 'transparent'
                }
            },

            series: [
                {
                    name: 'Values',
                    type: 'area',
                    // data: [[1,7],[2,49],[3,22],[4,18],[5,27],[6,63],[7,50],[8,43],[9,34],[10,42],[11,94],[12,76],[13,21],[14,38],[15,31],[16,81],[17,94],[18,21],[19,38],[20,41],[21,83],[22,14],[23,16],[24,22],[25,72],[26,71],[27,46],[28,19],[29,24],[30,82],[31,32],[32,53],[33,88],[34,31],[35,73],[36,50],[37,51],[38,86],[39,92],[40,47],[41,29],[42,79],[43,3],[44,91],[45,8],[46,37],[47,88],[48,34],[49,67],[50,9],[51,52],[52,69],[53,31],[54,68],[55,49],[56,38],[57,98],[58,3],[59,2],[60,100],[61,64],[62,73],[63,56],[64,60],[65,62],[66,50],[67,43],[68,90],[69,97],[70,72],[71,4],[72,55],[73,15],[74,37],[75,42],[76,57],[77,25],[78,56],[79,37],[80,34],[81,64],[82,42],[83,53],[84,36],[85,40],[86,39],[87,8],[88,1],[89,89],[90,79],[91,69],[92,55],[93,5],[94,0],[95,31],[96,74],[97,18],[98,91],[99,49],[100,4],[101,66],[102,98],[103,27],[104,80],[105,25],[106,92],[107,95],[108,32],[109,13],[110,99],[111,99],[112,18],[113,59],[114,85],[115,48],[116,27],[117,88],[118,31],[119,52],[120,18],[121,32],[122,35],[123,26],[124,94],[125,95],[126,86],[127,85],[128,48],[129,34],[130,54],[131,35],[132,10],[133,74],[134,97],[135,91],[136,45],]
                    data: this.state.values,
                    color: 'blue',
                },
                {
                    name: 'Danger Area',
                    type: 'arearange',
                    // data: [[22,45,51],[23,24,30],[24,10,16],[25,-3,3],[26,90,96],[27,21,27],[28,87,93],[29,10,16],[30,51,57],[31,75,81],[32,20,26],[33,23,29],[34,60,66],[35,92,98],[36,55,61],[37,62,68],[38,73,79],[39,90,96],[40,7,13],[41,30,36],[42,6,12],[43,58,64],[44,81,87],[45,16,22],[46,48,54],[47,55,61],[48,62,68],[49,64,70],[50,91,97],[51,82,88],[52,60,66],[53,51,57],[54,48,54],[55,1,7],[56,39,45],[57,21,27],[58,30,36],[59,92,98],],
                    data: this.state.highlightedArea,
                    lineWidth: 1,
                    zIndex: 0,
                    fillColor: 'red'
                }
            ]
        };

        return (
            <ReactHighcharts config={config} ref="chart" />
        );
    }
}
