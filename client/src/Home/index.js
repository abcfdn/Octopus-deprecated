import React from 'react';

import { withStyles } from '@material-ui/core/styles';
import { withAuth } from '@okta/okta-react';

import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import APIClient from '../apiClient'
import Session from '../Session'

const styles = theme => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    fontWeight: theme.typography.fontWeightRegular,
  },
});

class Home extends React.Component {
  state = {
    sessions: [],
  };

  async componentDidMount() {
    const accessToken = await this.props.auth.getAccessToken()
    this.apiClient = new APIClient(accessToken);
    this.apiClient.getSessions().then((data) => {
      this.setState({...this.state, sessions: data})
    });
  }

  renderSessions = (sessions) => {
    if (sessions.length) {
      return sessions.map((session) =>
        <ExpansionPanel key={session.created_at}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography className={styles.heading}>{session.name}</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <Session session={session} />
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
        {this.renderSessions(this.state.sessions)}
      </div>
    );
  }
}

export default withStyles(styles)(withAuth(Home));
