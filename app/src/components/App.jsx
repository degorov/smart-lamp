import React from 'react';
import { hot } from 'react-hot-loader/root';

import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import { ruRU } from '@material-ui/core/locale';

import { CssBaseline, Container, Typography, Button } from '@material-ui/core';

function App() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');

  const theme = React.useMemo(
    () =>
      createMuiTheme(
        {
          palette: {
            type: prefersDarkMode ? 'dark' : 'light',
          },
        },
        ruRU,
      ),
    [prefersDarkMode],
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container>
        <Typography variant="h3">Hello Lamp</Typography>
        <Button
          variant="contained"
          onClick={() => {
            alert('clicked');
          }}
        >
          Click me!
        </Button>
      </Container>
    </ThemeProvider>
  );
}

export default hot(App);
