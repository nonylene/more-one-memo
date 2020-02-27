import React from 'react';
import './App.css';
import IgnoreChannelsInput from '../ignore-channels-input/IgnoreChannelsInput';
import ChannelRegExpsInput from '../channel-regexps-input/ChannelRegExpsInput';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import CssBaseline from '@material-ui/core/CssBaseline';
import { Grid, Button } from '@material-ui/core';

const App = () => {
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
            <ChannelRegExpsInput />
          </Grid>
        </Grid>

        <Grid container className="App-inputBox" justify="center">
          <Grid item xs={12} md={8}>
            <IgnoreChannelsInput />
          </Grid>
        </Grid>

        <Grid container className="App-inputBox" justify="center">
          <Grid item xs={12} md={8}>
            <IgnoreChannelsInput />
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
