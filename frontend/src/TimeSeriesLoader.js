import React, { Component } from 'react';
import axios from 'axios';
import moment from 'moment';

import Timeseries from './TimeseriesChart';
import Features from './FeaturesChart';

import {getRedLine} from './redLines';

const DATA_QUALITY_THRESHOLD = 0.5;

export default class Loader extends Component {

    constructor(props) {
        super(props);

        this.state = {
            lastValueWasRed: false,
            valueBeforeLastWasBlue: true,
            redLinesList: [],
            nextRedLineList: [],
            blueLine: [],
            featuresLine: [],

            firstDate: Date.now(),
            lastDate: Date.now(),

            stopLoading: false,
        }
    }

    componentDidMount() {
        this.loadNewValue()
    }

    componentWillReceiveProps() {
        this.loadNewValue()
    }

    loadNewValue() {
        if (this.state.stopLoading) {
            return;
        }

        axios.get('http://localhost:8080/')
            .then(res => {
                let newRedLineList = this.state.redLinesList;
                let nextNextRedLineList = this.state.nextRedLineList;
                let newBlueLine = this.state.blueLine;
                let nextLastValueWasRed = false;


                // let time = Date(res.data.time);
                // const newValue = [time, res.data.value];
                const newValue = [res.data.time * 1000, res.data.value];
                newBlueLine = newBlueLine.concat([newValue]);

                if (res.data.value < DATA_QUALITY_THRESHOLD) {
                    nextLastValueWasRed = true;
                    nextNextRedLineList = nextNextRedLineList.concat([newValue]);
                } else if (this.state.lastValueWasRed) {
                    nextLastValueWasRed = false;
                    let aRedLine = getRedLine(this.state.nextRedLineList);
                    newRedLineList = newRedLineList.concat([aRedLine]);
                    nextNextRedLineList = [];
                }


                const newFeaturesLine = this.state.featuresLine.concat([res.data.fv]);

                this.setState({
                    nextRedLineList: nextNextRedLineList,
                    redLinesList: newRedLineList,
                    blueLine: newBlueLine,
                    lastValueWasRed: nextLastValueWasRed,
                    lastDate: Date.now(),
                    featuresLine: newFeaturesLine,
                });

                setTimeout(this.componentWillReceiveProps.bind(this), 100)
            });
    }

    render() {
        return (
            <div>
                <div onClick={this.toggleLoadingButtonHandler.bind(this)}>Loading toggle</div>
                <Timeseries redLinesList={this.state.redLinesList}
                            blueLine={this.state.blueLine}
                            nextRedLine={getRedLine(this.state.nextRedLineList)}
                            firstDate={this.state.firstDate}
                            maxDate={this.state.maxDate} />
                <Features featuresLine={this.state.featuresLine} />
            </div>
        );
    }

    toggleLoadingButtonHandler() {
        this.setState({stopLoading: !this.state.stopLoading})
        setTimeout(this.loadNewValue.bind(this), 0);
    }
}