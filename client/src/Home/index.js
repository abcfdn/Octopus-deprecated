import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import SwipeableViews from 'react-swipeable-views';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Grid from '@material-ui/core/Grid';
import { withAuth } from '@okta/okta-react';

import GithubRepo from "../GithubRepo"
import SearchBar from "../SearchBar"

import APIClient from '../apiClient'

const styles = theme => ({
  root: {
    flexGrow: 1,
    marginTop: 30
  },
  paper: {
    padding: theme.spacing.unit * 2,
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
});

class Home extends React.Component {
  state = {
    value: 0,
    events: [],
  };

  async componentDidMount() {
    const accessToken = await this.props.auth.getAccessToken()
    this.apiClient = new APIClient(accessToken);
    this.apiClient.getEvents().then((data) =>
      this.setState({...this.state, events: data})
    );
  }

  handleTabChange = (event, value) => {
    this.setState({ value });
  };

  handleTabChangeIndex = index => {
    this.setState({ value: index });
  };

  resetRepos = repos => this.setState({ ...this.state, repos })

  updateBackend = (repo) => {
    if (this.isKudo(repo)) {
      this.apiClient.deleteKudo(repo);
    } else {
      this.apiClient.createKudo(repo);
    }
    this.updateState(repo);
  }

  updateState = (repo) => {
    if (this.isKudo(repo)) {
      this.setState({
        ...this.state,
        kudos: this.state.kudos.filter( r => r.id !== repo.id )})
    } else {
      this.setState({
        ...this.state,
        kudos: [repo, ...this.state.kudos]
      })
    }
  }

  onSearch = (event) => {
    const target = event.target;
    if (!target.value || target.length < 3) { return }
    if (event.which !== 13) { return }

  }

  getEventDate = (event) => {

  }

  renderEvents = (events) => {
    if (!events) { return [] }
    return events.map((e) => {
      return (
        <ListItem button onClick={this.handleClick}>
          <ListItemText inset primary="" />
          {this.state.open ? <ExpandLess /> : <ExpandMore />}
        </ListItem>
        <Collapse in={this.state.open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
          </List>
        </Collapse>
      );
    })
  }

  render() {
    return (
      <div className={styles.root}>
        <SearchBar auth={this.props.auth} onSearch={this.onSearch} />
         <Tabs
          value={this.state.value}
          onChange={this.handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          fullWidth
        >
          <Tab label="Events" />
        </Tabs>

        <List
         component="nav"
         subheader={<ListSubheader component="div">Nested List Items</ListSubheader>}
         className={classes.root}
        >
          { this.renderEvents(this.state.events) }
        </List>
      </div>
    );
  }
}

export default withStyles(styles)(withAuth(Home));
