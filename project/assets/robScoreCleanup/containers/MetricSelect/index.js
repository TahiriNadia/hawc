import React, { Component } from 'react';
import { connect } from 'react-redux';

import { selectMetric } from 'robScoreCleanup/actions/Metrics';

import ArraySelect from 'shared/components/ArraySelect';

export class MetricSelect extends Component {
  
    constructor(props) {
        super(props);
        this.handleSelect = this.handleSelect.bind(this);
    }

    setDefaultValue() {
        this.choices = this.formatMetricChoices();
        this.defaultValue = _.first(this.choices).id;
        this.handleSelect(this.defaultValue);
    }

    formatMetricChoices(){
        return _.map(this.props.choices, (choice) => {
            return {id: choice.id, value: choice.metric};
        });
    }

    handleSelect(option=null){
        let choice = _.findWhere(this.props.choices, {id: parseInt(option)});
        this.props.dispatch(selectMetric(choice));
    }

    render() {
        if (!this.props.isLoaded) return null;
        this.setDefaultValue();
        return (
            <ArraySelect id='metric-select'
                    choices={this.choices}
                    handleSelect={this.handleSelect}
                    defVal={this.defaultValue}/>
        );
    }
}

function mapStateToProps(state) {
    return {
        isLoaded: state.metrics.isLoaded,
        choices: state.metrics.items,
    };
}

export default connect(mapStateToProps)(MetricSelect);
