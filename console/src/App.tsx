import React from 'react';
import './App.css';

import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import CssBaseline from '@material-ui/core/CssBaseline';
import { Grid } from '@material-ui/core';

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
      <Container>
        <Grid container>
          <Grid item>

            <Button variant="contained" color="primary">
              Hello!
        </Button>

          </Grid>

        </Grid>
      </Container>
    </div>
  );
}

export default App;
