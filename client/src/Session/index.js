import React from 'react';
import ReactMarkdown from 'react-markdown';

import { withStyles } from '@material-ui/core/styles';
import { withAuth } from '@okta/okta-react';

import Paper from '@material-ui/core/Paper';
import Link from 'react-router-dom/Link';
import Button from '@material-ui/core/Button';
import queryString from 'query-string';

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
    generatingPoster: false,
    credential_id: null,
  };

  async componentDidMount() {
    const params = queryString.parse(this.props.location.search)
    this.setState({...this.state, credential_id: params['credential_id']})

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

  handleClick = () => {
    this.setState({...this.state, generatingPoster: true})
    const session_id = this.props.match.params.session_id;
    this.props.auth.getAccessToken().then((token) => {
      this.apiClient = new APIClient(token);
      this.apiClient.getPoster(session_id, this.state.credential_id).then((data) => {
        if (data['success']) {
          this.setState({...this.state, generatingPoster: false})
        } else {
          var authorize_url = data['authorize_url']
          var param = 'origin_url=' + window.location.href
          authorize_url += (authorize_url.split('?')[1] ? '&':'?') + param
          window.location = authorize_url
        }
      });
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
          <Button
            disabled={this.state.generatingPoster}
            variant="contained"
            color="primary"
            onClick={this.handleClick}
            className={styles.button}>
            Generate Poster
          </Button>

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
