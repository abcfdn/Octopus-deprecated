import React from 'react';

import { withStyles } from '@material-ui/core/styles';
import { withAuth } from '@okta/okta-react';

import TextField from '@material-ui/core/TextField';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
});


class Schedule extends React.Component {
  getDefaultStartTime(schedule) {
  }

  render() {
    const { classes } = this.props;
    return (
    <div>
      <form className={classes.container} noValidate>
        <TextField
          id="datetime-local"
          label="Start Time"
          type="datetime-local"
          defaultValue="2017-05-24T10:30"
          className={classes.textField}
          InputLabelProps={{shrink: true,}}
        />
      </form>

      <form className={classes.container} noValidate>
        <TextField
          id="datetime-local"
          label="End Time"
          type="datetime-local"
          defaultValue="2017-05-24T10:30"
          className={classes.textField}
          InputLabelProps={{shrink: true,}}
        />
      </form>
    </div>
    );
  }
}

export default withStyles(styles)(withAuth(Schedule));
