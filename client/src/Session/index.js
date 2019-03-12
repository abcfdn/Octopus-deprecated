import React from 'react';
import ReactMarkdown from 'react-markdown';

import { withStyles } from '@material-ui/core/styles';
import { withAuth } from '@okta/okta-react';

import Paper from '@material-ui/core/Paper';

import APIClient from '../apiClient'

const styles = theme => ({
  root: {
    ...theme.mixins.gutters(),
    paddingTop: theme.spacing.unit * 2,
    paddingBottom: theme.spacing.unit * 2,
    maxWidth: 800,
  }
});


class Session extends React.Component {
  state = {
    presenter: {},
  };

  async componentDidMount() {
    const accessToken = await this.props.auth.getAccessToken()
    this.apiClient = new APIClient(accessToken);
    this.apiClient.getPresenter(
      this.props.session['presenter']).then((data) =>
        this.setState({...this.state, presenter: data})
      );
  }

  composeLine = (key, value) => {
    if (typeof value === 'string' && /^https?:\/\//.test(value)) {
      return '__' + key + '__: [Link](' + value + ')';
    } else {
      return '__' + key + '__: ' + value;
    }
  }

  composeLines = (title, object, excluded_properties) => {
    var lines = []
    lines.push('## ' + title)
    for (var property in object) {
      if (excluded_properties.includes(property)) { continue; }
      if (object.hasOwnProperty(property)) {
        lines.push(this.composeLine(property, object[property]));
      }
    }
    return lines
  }

  composeInput = (session, presenter) => {
    var lines = [];
    lines = lines.concat(this.composeLines('Session', session, ['schedule']));
    lines = lines.concat(this.composeLines('Schedule', session.schedule, []));
    lines = lines.concat(this.composeLines('Presenter', presenter, ['project']));
    lines = lines.concat(this.composeLines('Project', presenter.project, []));
    return lines.join('\n\n')
  }

  render() {
    const { classes } = this.props;
    return (
      <div>
        <Paper className={classes.root} elevation={1}>
          <ReactMarkdown
            source={this.composeInput(this.props.session, this.state.presenter)}
          />
        </Paper>
      </div>
    );
  }
}

export default withStyles(styles)(withAuth(Session));
