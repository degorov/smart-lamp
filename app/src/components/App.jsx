import React, { useState, useMemo, useEffect } from 'react';
import { hot } from 'react-hot-loader/root';
import { makeStyles } from '@material-ui/core/styles';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import { ruRU } from '@material-ui/core/locale';

import Backdrop from '@material-ui/core/Backdrop';
import Box from '@material-ui/core/Box';
import CircularProgress from '@material-ui/core/CircularProgress';
import Container from '@material-ui/core/Container';
import CssBaseline from '@material-ui/core/CssBaseline';

import { ConnectedContext } from './AppContexts';
import Api from '../api';
import TopBar from './TopBar';
import BottomNav from './BottomNav';
import Effects from './Effects';
import Alarm from './Alarm';
import Settings from './Settings';

const useStyles = makeStyles((theme) => ({
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
}));

function App() {
  const classes = useStyles();

  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
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

  const pageTitles = ['Эффекты', 'Будильник', 'Настройки'];

  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(null);
  const [ip, setIp] = useState({ address: '', valid: false });
  const [connected, setConnected] = useState();
  const [changed, setChanged] = useState(false);

  useEffect(() => {
    const lsIp = localStorage.getItem('lamp-ip');
    if (lsIp) {
      setIp({ address: lsIp, valid: true });
    } else {
      setConnected(false);
    }

    window.fetchWithLoading = async (...args) => {
      setLoading(true);
      try {
        return await fetch(...args);
      } finally {
        setLoading(false);
      }
    };
  }, []);

  useEffect(() => {
    if (connected === undefined && ip.address) {
      (async () => {
        const pong = await Api.ping(ip.address);
        if (pong) {
          localStorage.setItem('lamp-ip', ip.address);
          setConnected(true);
          if (page === null) {
            setPage(0);
          }
        } else {
          setConnected(false);
        }
      })();
    } else if (connected === false) {
      setPage(2);
    }
    setChanged(false);
  }, [ip.address, connected, page]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container disableGutters maxWidth="sm">
        <ConnectedContext.Provider value={connected}>
          <TopBar title={pageTitles[page]} changed={changed} />
          <Box pb="56px">
            {page === 0 ? (
              <Effects />
            ) : page === 1 ? (
              <Alarm />
            ) : page === 2 ? (
              <Settings
                ip={ip}
                setIp={setIp}
                doConnect={() => setConnected()}
                doChange={() => setChanged(true)}
              />
            ) : null}
          </Box>
          <BottomNav page={page} labels={pageTitles} setPage={setPage} />
        </ConnectedContext.Provider>
      </Container>
      <Backdrop className={classes.backdrop} open={loading}>
        <CircularProgress color="inherit" />
      </Backdrop>
    </ThemeProvider>
  );
}

export default hot(App);
