import React from 'react';

import { withStyles } from '@material-ui/core/styles';
import { withAuth } from '@okta/okta-react';

import Paper from '@material-ui/core/Paper';

import APIClient from '../apiClient'

const styles = theme => ({
  root: {
    ...theme.mixins.gutters(),
    paddingTop: theme.spacing.unit * 2,
    paddingBottom: theme.spacing.unit * 2,
  }
});


class Session extends React.Component {
  state = {
    presenter: {},
  };

  async componentDidMount() {
    const accessToken = await this.props.auth.getAccessToken()
    this.apiClient = new APIClient(accessToken);
    this.apiClient.getPresenter().then((data) =>
      this.setState({...this.state, presenter: data})
    );
  }

  composeInput = (session, presenter) => {
    var lines = [];
    lines.push('# Session')
    for (var property in session) {
      if (property === 'schedule') { continue; }
      if (session.hasOwnProperty(property)) {
        lines.push('## ' + property);
        lines.push(session[property]);
      }
    }

    lines.push('# Schedule')
    for (property in session.schedule) {
      if (session.hasOwnProperty(property)) {
        lines.push('## ' + property);
        lines.push(session[property]);
      }
    }

    lines.push('# Presenter')
    for (property in presenter) {
      if (property === 'project') { continue; }
      if (session.hasOwnProperty(property)) {
        lines.push('## ' + property);
        lines.push(session[property]);
      }
    }

    lines.push('# Project')
    for (property in presenter.project) {
      if (session.hasOwnProperty(property)) {
        lines.push('## ' + property);
        lines.push(session[property]);
      }
    }
    return lines.join('\n')
  }

  render() {
    const { classes } = this.props;
    return (
      <div>
        <Paper className={classes.root} elevation={1}>
          {this.composeInput(this.props.session, this.state.presenter)}
        </Paper>
      </div>
    );
  }
}

export default withStyles(styles)(withAuth(Session));
