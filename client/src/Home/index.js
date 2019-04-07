import React from 'react';

import { withStyles } from '@material-ui/core/styles';
import { withAuth } from '@okta/okta-react';

import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Button from '@material-ui/core/Button';
import Link from 'react-router-dom/Link';

import queryString from 'query-string';

import APIClient from '../apiClient'
import SessionDetail from '../SessionDetail'

const styles = theme => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    fontWeight: theme.typography.fontWeightRegular,
  },
  button: {
    margin: theme.spacing.unit,
  },
});

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.logout = this.logout.bind(this);
  }

  state = {
    sessions: [],
    refreshed: true,
    credential_id: null,
  };

  async componentDidMount() {
    const params = queryString.parse(this.props.location.search)
    this.setState({...this.state, credential_id: params['credential_id']})

    const accessToken = await this.props.auth.getAccessToken()
    this.apiClient = new APIClient(accessToken);
    this.apiClient.getSessions().then((data) => {
      this.setState({...this.state, sessions: data})
    });
  }

  handleClick = () => {
    this.setState({...this.state, refreshed: false})
    this.props.auth.getAccessToken().then((token) => {
      this.apiClient = new APIClient(token);
      this.apiClient.refresh(this.state.credential_id).then((data) => {
        if (data['success']) {
          this.setState({...this.state, refreshed: true})
        } else {
          var authorize_url = data['authorize_url']
          var param = 'origin_url=' + window.location.href
          authorize_url += (authorize_url.split('?')[1] ? '&':'?') + param
          window.location = authorize_url
        }
      });
    });
  }

  async logout(e) {
    e.preventDefault();
    this.props.auth.logout('/');
  }

  renderTipText = () => {
    var text = this.state.refreshed ? 'Synced' : 'Syncing';
    return <Typography className={styles.heading}>{text}</Typography>
  }

  renderSessionList = (sessions) => {
    if (sessions.length) {
      return sessions.map((session) =>
        <ExpansionPanel key={session.created_at}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography className={styles.heading}>{session.name}</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <SessionDetail session={session} />
          </ExpansionPanelDetails>
        </ExpansionPanel>
      );
    } else {
      return <Typography>No Sessions</Typography>
    }
  }

  render() {
    return (
      <div className={styles.root}>
        <Button onClick={this.logout} color="inherit">Logout</Button>
        <Button
         disabled={!this.state.refreshed}
         variant="contained"
         color="primary"
         onClick={this.handleClick}
         className={styles.button}>
          Sync
        </Button>
        {this.renderTipText()}
        <Link to='/members'>
          Members
        </Link>
        {this.renderSessionList(this.state.sessions)}
      </div>
    );
  }
}

export default withStyles(styles)(withAuth(Home));
