import React, { useState } from 'react';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import CssBaseline from '@material-ui/core/CssBaseline';
import { Grid, Button } from '@material-ui/core';

import './App.css';
import IgnoreChannelsInput from '../ignore-channels-input/IgnoreChannelsInput';
import IgnoreUsersInput from "../ignore-users-input/IgnoreUsersInput";
import ChannelRegExpsInput from '../channel-regexps-input/ChannelRegExpsInput';
import { Channel, User } from '../../models/models';

const App = () => {

  const [channelRegExps, setChannelRegExps] = useState<string[]>([]);
  const [ignoreChannels, setIgnoreChannels] = useState<Channel[]>([]);
  const [ignoreUsers, setIgnoreUsers] = useState<User[]>([]);

  return (
    <div className="App">
      <CssBaseline />

      <AppBar position="static">
        <Toolbar variant="dense">
          <Typography variant="h6" color="inherit">
            more-one-memo console
          </Typography>
        </Toolbar>
      </AppBar>

      <Container className="App-container">
        <Grid container className="App-inputBox" justify="center">
          <Grid item xs={12} md={8}>
            <ChannelRegExpsInput value={channelRegExps} onChange={setChannelRegExps} />
          </Grid>
        </Grid>

        <Grid container className="App-inputBox" justify="center">
          <Grid item xs={12} md={8}>
            <IgnoreChannelsInput value={ignoreChannels} onChange={setIgnoreChannels} />
          </Grid>
        </Grid>

        <Grid container className="App-inputBox" justify="center">
          <Grid item xs={12} md={8}>
            <IgnoreUsersInput value={ignoreUsers} onChange={setIgnoreUsers} />
          </Grid>
        </Grid>

        <Grid container justify="center">
          <Grid item container xs={12} md={8} justify="flex-end">
            <Button variant="contained" color="primary">
              Save
            </Button>
          </Grid>
        </Grid>
      </Container >
    </div >
  );
}

export default App;
