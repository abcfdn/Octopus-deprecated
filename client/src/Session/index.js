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

  composeInput = (session, presenter) => {
    var lines = [];
    lines.push('## Session')
    for (var property in session) {
      if (property === 'schedule') { continue; }
      if (session.hasOwnProperty(property)) {
        lines.push('__' + property + '__: ' + session[property]);
      }
    }

    lines.push('## Schedule');
    for (property in session.schedule) {
      if (session.schedule.hasOwnProperty(property)) {
        lines.push('__' + property + '__: ' + session.schedule[property]);
      }
    }

    lines.push('## Presenter')
    for (property in presenter) {
      if (presenter === 'project') { continue; }
      if (presenter.hasOwnProperty(property)) {
        lines.push('__' + property + '__: ' + presenter[property]);
      }
    }

    lines.push('## Project')
    for (property in presenter.project) {
      if (presenter.project.hasOwnProperty(property)) {
        lines.push('__' + property + '__: ' + presenter.project[property]);
      }
    }
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
