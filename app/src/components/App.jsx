import React, { useState, useMemo, useEffect } from 'react';
import { hot } from 'react-hot-loader/root';
import { makeStyles } from '@material-ui/core/styles';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import { ruRU } from '@material-ui/core/locale';

import Backdrop from '@material-ui/core/Backdrop';
import Box from '@material-ui/core/Box';
import CircularProgress from '@material-ui/core/CircularProgress';
import Container from '@material-ui/core/Container';
import CssBaseline from '@material-ui/core/CssBaseline';

import { ConnectionContext, ApiContext } from './AppContexts';

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
  offset: {
    paddingBottom: theme.mixins.toolbar.minHeight,
  },
}));

function App() {
  const classes = useStyles();

  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const theme = useMemo(
    () =>
      createTheme(
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
  const [save, setSave] = useState(null);

  const API = useMemo(() => Api(setLoading, () => localStorage.getItem('lamp-ip')), []);

  useEffect(() => {
    if (connected === undefined && !ip.address && page === null) {
      const lsIp = localStorage.getItem('lamp-ip');
      if (lsIp) {
        setIp({ address: lsIp, valid: true });
      } else {
        setConnected(false);
      }
    }

    if (connected === undefined && ip.address) {
      (async () => {
        const pong = await API.ping(ip.address);
        if (pong) {
          localStorage.setItem('lamp-ip', ip.address);
          setConnected(true);
        } else {
          setConnected(false);
        }
      })();
    }

    if (connected === true && page === null) {
      setPage(0);
    }

    if (connected === false && page !== 2) {
      setPage(2);
    }
  }, [API, connected, ip.address, page]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container disableGutters>
        <ConnectionContext.Provider value={[connected, setConnected]}>
          <TopBar title={pageTitles[page]} save={save} />
          <Box className={classes.offset}>
            <ApiContext.Provider value={API}>
              {page === 0 ? (
                <Effects />
              ) : page === 1 ? (
                <Alarm setSave={setSave} />
              ) : page === 2 ? (
                <Settings ip={ip} setIp={setIp} setSave={setSave} />
              ) : null}
            </ApiContext.Provider>
          </Box>
          <BottomNav labels={pageTitles} page={page} setPage={setPage} />
        </ConnectionContext.Provider>
      </Container>
      <Backdrop className={classes.backdrop} open={loading}>
        <CircularProgress color="inherit" />
      </Backdrop>
    </ThemeProvider>
  );
}

export default hot(App);
