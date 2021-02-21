import React, { useState } from 'react';
import { hot } from 'react-hot-loader/root';

import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import { ruRU } from '@material-ui/core/locale';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';

import Button from '@material-ui/core/Button';
import Box from '@material-ui/core/Box';

import TopBar from './TopBar';
import BottomNav from './BottomNav';

function App() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');

  const pageTitles = ['Эффекты', 'Будильник', 'Настройки'];
  const [page, setPage] = useState(0);
  const [connected, setConnected] = useState(false);

  const theme = React.useMemo(
    () =>
      createMuiTheme(
        {
          palette: {
            primary: {
              main: prefersDarkMode ? '#FFCD14' : '#F55528',
            },
            secondary: {
              main: prefersDarkMode ? '#0AAAD7' : '#008CC3',
            },
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
      <Container disableGutters maxWidth="lg">
        <TopBar title={pageTitles[page]} connected={connected} />

        <Box m={1}>
          <Button variant="contained" color="primary">
            Primary
        </Button>
          <Button variant="contained" color="secondary">
            Secondary
          </Button>
        </Box>
        <BottomNav page={page} labels={pageTitles} onChange={setPage} />
      </Container>
    </ThemeProvider>
  );
}

export default hot(App);
