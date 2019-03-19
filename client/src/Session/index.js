import React from 'react';
import ReactMarkdown from 'react-markdown';

import { withStyles } from '@material-ui/core/styles';
import { withAuth } from '@okta/okta-react';

import Paper from '@material-ui/core/Paper';
import Link from 'react-router-dom/Link';

import APIClient from '../apiClient'
import MarkdownUtil from '../util'
import Schedule from '../Schedule';

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
    session: {},
    presenter: {},
  };

  async componentDidMount() {
    const accessToken = await this.props.auth.getAccessToken();
    const session_id = this.props.match.params.session_id;
    this.apiClient = new APIClient(accessToken);
    this.apiClient.getSession(session_id).then((data) => {
      this.setState({...this.state, session: data});
      this.apiClient.getPresenter(data.presenter).then((data) =>
        this.setState({...this.state, presenter: data})
      );
    });
  }

  render() {
    const { classes } = this.props;
    const markdownUtil = new MarkdownUtil();
    return (
      <div>
        <Link to='/'>
          Back
        </Link>

        <Paper className={classes.root} elevation={1}>
          <Schedule schedule={this.state.session.schedule}/>
          <ReactMarkdown
            source={markdownUtil.composeInput(
              this.state.session, this.state.presenter)}
          />
        </Paper>
      </div>
    );
  }
}

export default withStyles(styles)(withAuth(Session));
