import React, { Component } from 'react';
import Timeseries from './TimeseriesChart';
import axios from 'axios';

const DATA_QUALITY_THRESHOLD = 0.5;

export default class Loader extends Component {

    constructor(props) {
        super(props);

        this.state = {
            lastRedValueArray: undefined,
            needToAddLastRedValue: false,
            redLine: [],
            blueLine: [],
        }
    }

    componentDidMount() {
        this.loadNewValue()
    }

    componentWillReceiveProps() {
        this.loadNewValue()
    }

    loadNewValue() {
        axios.get('http://localhost:8080/')
            .then(res => {
                let newRedDots = this.state.redLine;
                let newBlueLine = this.state.blueLine;

                const newValue = [res.data.time, res.data.value];
                newBlueLine = newBlueLine.concat([newValue]);
                let newNeedToAddLastRedValue = this.state.needToAddLastRedValue;
                if (res.data.dq < DATA_QUALITY_THRESHOLD) {
                    if (this.state.needToAddLastRedValue) {
                        newRedDots.concat([this.state.lastRedValueArray, newValue]);
                        newNeedToAddLastRedValue = false;
                    } else {
                        newRedDots.concat([newValue]);
                        newNeedToAddLastRedValue = true;
                    }
                }


                this.setState({
                    redLine: newRedDots,
                    blueLine: newBlueLine,
                    needToAddLastRedValue: newNeedToAddLastRedValue,
                });

                setTimeout(this.componentWillReceiveProps.bind(this), 1)
            });
    }

    render() {
        return (
            <div>
                <Timeseries redDots={this.state.redLine} blueLine={this.state.blueLine} />
            </div>
        );
    }
}
