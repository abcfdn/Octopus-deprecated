import React from 'react';
import ReactMarkdown from 'react-markdown';

import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';

import { withAuth } from '@okta/okta-react';
import Link from 'react-router-dom/Link';

import MarkdownUtil from '../util'

const styles = theme => ({
  root: {
    ...theme.mixins.gutters(),
    paddingTop: theme.spacing.unit * 2,
    paddingBottom: theme.spacing.unit * 2,
    maxWidth: 800,
  }
});


class MemberDetail extends React.Component {
  async componentDidMount() { }

  render() {
    const { classes } = this.props;
    const markdownUtil = new MarkdownUtil();
    return (
      <div>
        <Paper className={classes.root} elevation={1}>
          <ReactMarkdown
            source={markdownUtil.composeMember(this.props.member)}
          />
        </Paper>
      </div>
    );
  }
}

export default withStyles(styles)(withAuth(MemberDetail));
