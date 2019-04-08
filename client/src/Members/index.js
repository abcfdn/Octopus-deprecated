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

import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';

import queryString from 'query-string';

import APIClient from '../apiClient'
import MemberDetail from '../MemberDetail'

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

class Members extends React.Component {
  constructor(props) {
    super(props);
  }

  state = {
    members: [],
    refreshed: true,
    error: null,
  };

  async componentDidMount() {
    const params = queryString.parse(this.props.location.search)
    this.setState({...this.state, credential_id: params['credential_id']})

    const accessToken = await this.props.auth.getAccessToken()
    this.apiClient = new APIClient(accessToken);
    this.apiClient.getMembers().then((data) => {
      this.setState({...this.state, members: data})
    });
  }

  handleClick = () => {
    this.setState({...this.state, refreshed: false})
    this.props.auth.getAccessToken().then((token) => {
      this.apiClient = new APIClient(token);
      this.apiClient.reloadMembers(this.state.credential_id).then((data) => {
        if (data['success']) {
          this.setState({...this.state, refreshed: true})
        }
      });
    });
  }

  handleAlertDialogClose = () => {
    this.setState({ error: null })
  }

  renderAlertDialog = () => {
    return (
      <Dialog
        open={this.state.error !== null}
        onClose={this.handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Task failed with error: {this.state.error}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={this.handleAlertDialogClose} color="primary" autoFocus>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    )
  }

  renderTipText = () => {
    var text = this.state.refreshed ? 'Synced' : 'Syncing';
    return <Typography className={styles.heading}>{text}</Typography>
  }

  renderMemberList = (members) => {
    if (members.length) {
      return members.map((member) =>
        <ExpansionPanel key={member.email}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <Typography className={styles.heading}>{member.name}</Typography>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <MemberDetail member={member} />
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
        <Link to='/'>
          Back
        </Link>
        <Button
         disabled={!this.state.refreshed}
         variant="contained"
         color="primary"
         onClick={this.handleClick}
         className={styles.button}>
          Sync
        </Button>
        {this.renderTipText()}
        {this.renderAlertDialog()}
        {this.renderMemberList(this.state.members)}
      </div>
    );
  }
}

export default withStyles(styles)(withAuth(Members));
