import React from 'react';
import ReactMarkdown from 'react-markdown';

import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';

import { withAuth } from '@okta/okta-react';
import Link from 'react-router-dom/Link';

import APIClient from '../apiClient'
import MarkdownUtil from '../util'

const styles = theme => ({
  root: {
    ...theme.mixins.gutters(),
    paddingTop: theme.spacing.unit * 2,
    paddingBottom: theme.spacing.unit * 2,
    maxWidth: 800,
  }
});


class SessionDetail extends React.Component {
  state = {
    presenter: {},
  };

  async componentDidMount() {
    const accessToken = await this.props.auth.getAccessToken()
    this.apiClient = new APIClient(accessToken);
    this.apiClient.getPresenter(
      this.props.session.presenter).then((data) =>
        this.setState({...this.state, presenter: data})
      );
  }

  render() {
    const { classes } = this.props;
    const markdownUtil = new MarkdownUtil();
    var sessionPath = "/session/" + this.props.session.created_at;
    return (
      <div>
        <Paper className={classes.root} elevation={1}>
           <Link to={sessionPath}>
             Publish
           </Link>

          <ReactMarkdown
            source={markdownUtil.composeInput(
              this.props.session, this.state.presenter)}
          />
        </Paper>
      </div>
    );
  }
}

export default withStyles(styles)(withAuth(SessionDetail));
