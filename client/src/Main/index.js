import React, { Component } from 'react';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom'
import { Security, ImplicitCallback, SecureRoute } from '@okta/okta-react';

import Login from '../Login'
import Home from '../Home'
import Members from '../Members'
import Session from '../Session'

class Main extends Component {
   render() {
        return (
               <Router>
                 <Security
                   issuer={'https://dev-319775.okta.com'}
                   client_id={'0oadlcq59mtzs8ack356'}
                   redirect_uri={'https://blockchainabc.org:8080/implicit/callback'}
                   scope={['openid', 'profile', 'email']}>

                   <Switch>
                     <Route exact path="/" component={Login} />
                     <Route path="/implicit/callback" component={ImplicitCallback} />
                     <SecureRoute path="/home" component={Home} />
                     <SecureRoute path="/members" component={Members} />
                     <SecureRoute path="/session/:session_id" component={Session} />
                   </Switch>
                 </Security>
               </Router>
             );
      }
}

export default Main;
