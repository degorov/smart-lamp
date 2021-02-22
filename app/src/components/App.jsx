import React, { useState, useMemo, useEffect } from 'react';
import { hot } from 'react-hot-loader/root';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import { ruRU } from '@material-ui/core/locale';

import Box from '@material-ui/core/Box';
import Container from '@material-ui/core/Container';
import CssBaseline from '@material-ui/core/CssBaseline';

import Api from '../api';
import TopBar from './TopBar';
import BottomNav from './BottomNav';
import Effects from './Effects';
import Alarm from './Alarm';
import Settings from './Settings';

function App() {
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');

  const pageTitles = ['Эффекты', 'Будильник', 'Настройки'];
  const [page, setPage] = useState(null);
  const [connected, setConnected] = useState(false);
  const [changed, setChanged] = useState(false);

  const theme = useMemo(
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

  useEffect(() => {
    (async () => {
      const lsIp = localStorage.getItem('lamp-ip');
      if (lsIp) {
        const connected = await Api.ping(lsIp);
        if (connected) {
          setPage(0);
          setConnected(true);
        } else {
          setPage(2);
        }
      } else {
        setPage(2);
      }
    })();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container disableGutters maxWidth="sm">
        <TopBar title={pageTitles[page]} changed={changed} connected={connected} />
        <Box pb="56px">
          {page === 0 ? (
            <Effects />
          ) : page === 1 ? (
            <Alarm />
          ) : page === 2 ? (
            <Settings setChanged={setChanged} connected={connected} setConnected={setConnected} />
          ) : null}
        </Box>
        <BottomNav page={page} labels={pageTitles} connected={connected} setPage={setPage} />
      </Container>
    </ThemeProvider>
  );
}

export default hot(App);
