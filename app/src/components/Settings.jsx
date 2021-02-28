import React, { useState, useEffect, useContext, useCallback } from 'react';
import { makeStyles } from '@material-ui/core/styles';

import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import FormControl from '@material-ui/core/FormControl';
import Grid from '@material-ui/core/Grid';
import IconButton from '@material-ui/core/IconButton';
import InputAdornment from '@material-ui/core/InputAdornment';
import InputLabel from '@material-ui/core/InputLabel';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListSubheader from '@material-ui/core/ListSubheader';
import MenuItem from '@material-ui/core/MenuItem';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import Slider from '@material-ui/core/Slider';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';

import BrightnessHighIcon from '@material-ui/icons/BrightnessHigh';
import BrightnessLowIcon from '@material-ui/icons/BrightnessLow';
import PhonelinkRingOutlinedIcon from '@material-ui/icons/PhonelinkRingOutlined';
import Visibility from '@material-ui/icons/Visibility';
import VisibilityOff from '@material-ui/icons/VisibilityOff';

import { ConnectionContext, ApiContext } from './AppContexts';
import Credits from './Credits';

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.paper,
  },
  icon: {
    marginTop: '-20px',
  },
}));

export default function Settings({ ip, setIp, setSave }) {
  const classes = useStyles();

  const [connected, setConnected] = useContext(ConnectionContext);
  const API = useContext(ApiContext);

  const [alert, setAlert] = React.useState(false);
  const openAlert = () => setAlert(true);
  const closeAlert = () => setAlert(false);

  const handleChangeIp = (event) => {
    const ip = event.target.value;
    if (/^(?!0)(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$/.test(ip)) {
      setIp({ address: ip, valid: true });
    } else {
      setIp({ address: ip, valid: false });
    }
  };

  const [settings, setSettings] = useState({
    ssid: '',
    password: '',
    showPassword: false,
    timezone: 3,
    brightness: 0,
  });

  const handleChangeSettings = (prop) => (event) => {
    setSettings({ ...settings, [prop]: event.target.value });
    setSave(saveSettings);
  };

  const handleClickShowPassword = () => {
    setSettings({ ...settings, showPassword: !settings.showPassword });
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const handleChangeBrightness = (event, newValue) => {
    setSettings({ ...settings, brightness: newValue });
    setSave(saveSettings);
  };

  const loadSettings = useCallback(async () => {
    if (connected) {
      const result = await API.getsettings();
      if (!result) {
        setConnected(false);
      } else {
        setSettings((settings) => ({
          ...settings,
          ssid: result.ssid,
          password: result.password,
          timezone: result.timezone,
          brightness: result.maxbrightness,
        }));
      }
    }
  }, [API, connected, setConnected]);

  const saveSettings = () => async () => {
    setSettings((settings) => {
      (async () => {
        const result = await API.savesettings(
          settings.ssid,
          settings.password,
          settings.timezone,
          settings.brightness,
        );
        if (result) {
          openAlert();
        }
        setConnected(false);
      })();
      return settings;
    });
    setSave(null);
  };

  useEffect(() => {
    window.addEventListener('focus', loadSettings);
    loadSettings();

    return () => {
      window.removeEventListener('focus', loadSettings);
      setSave(null);
    };
  }, [loadSettings, setSave]);

  return (
    <>
      <List className={classes.root}>
        <ListSubheader>Подключение:</ListSubheader>
        <ListItem>
          <TextField
            id="lamp-ip"
            label="IP-адрес лампы"
            variant="outlined"
            size="small"
            value={ip.address}
            onChange={handleChangeIp}
            error={!ip.valid}
          />
          <ListItemSecondaryAction>
            <Button
              variant="contained"
              color="primary"
              disabled={!ip.valid}
              onClick={() => setConnected()}
            >
              <PhonelinkRingOutlinedIcon />
            </Button>
          </ListItemSecondaryAction>
        </ListItem>
        {connected ? (
          <>
            <ListItem>
              <TextField
                id="ssid"
                label="Имя сети"
                variant="outlined"
                size="small"
                fullWidth={true}
                value={settings.ssid}
                onChange={handleChangeSettings('ssid')}
              />
            </ListItem>
            <ListItem>
              <FormControl variant="outlined" size="small" fullWidth={true}>
                <InputLabel htmlFor="password">Пароль сети</InputLabel>
                <OutlinedInput
                  id="password"
                  labelWidth={95}
                  type={settings.showPassword ? 'text' : 'password'}
                  value={settings.password}
                  onChange={handleChangeSettings('password')}
                  endAdornment={
                    <InputAdornment position="end">
                      <IconButton
                        onClick={handleClickShowPassword}
                        onMouseDown={handleMouseDownPassword}
                        edge="end"
                      >
                        {settings.showPassword ? <Visibility /> : <VisibilityOff />}
                      </IconButton>
                    </InputAdornment>
                  }
                />
              </FormControl>
            </ListItem>

            <ListSubheader>Часовой пояс:</ListSubheader>
            <ListItem>
              <TextField
                id="timezone"
                select
                variant="outlined"
                size="small"
                fullWidth={true}
                value={settings.timezone}
                onChange={handleChangeSettings('timezone')}
              >
                <MenuItem value={2}>МСК−1 (калининградское время)</MenuItem>
                <MenuItem value={3}>МСК (московское время)</MenuItem>
                <MenuItem value={4}>МСК+1 (самарское время)</MenuItem>
                <MenuItem value={5}>МСК+2 (екатеринбургское время)</MenuItem>
                <MenuItem value={6}>МСК+3 (омское время)</MenuItem>
                <MenuItem value={7}>МСК+4 (красноярское время)</MenuItem>
                <MenuItem value={8}>МСК+5 (иркутское время)</MenuItem>
                <MenuItem value={9}>МСК+6 (якутское время)</MenuItem>
                <MenuItem value={10}>МСК+7 (владивостокское время)</MenuItem>
                <MenuItem value={11}>МСК+8 (магаданское время)</MenuItem>
                <MenuItem value={12}>МСК+9 (камчатское время)</MenuItem>
              </TextField>
            </ListItem>

            <ListSubheader>
              Максимальная яркость:
              <Typography component="span" color={settings.brightness > 184 ? 'error' : 'initial'}>
                &nbsp;{settings.brightness}
              </Typography>
            </ListSubheader>
            <ListItem>
              <Grid container spacing={2} alignItems="center">
                <Grid item className={classes.icon}>
                  <BrightnessLowIcon />
                </Grid>
                <Grid item xs>
                  <Slider
                    min={72}
                    max={255}
                    marks={[
                      {
                        value: 184,
                        label: 'Предел БП',
                      },
                    ]}
                    value={settings.brightness}
                    onChange={handleChangeBrightness}
                  />
                </Grid>
                <Grid item className={classes.icon}>
                  <BrightnessHighIcon />
                </Grid>
              </Grid>
            </ListItem>
          </>
        ) : null}
      </List>

      <Credits />

      <Dialog open={alert} onClose={closeAlert}>
        <DialogTitle>{'Внимание!'}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Для применения настроек светильник необходимо перезагрузить вручную. Отключите
            светильник от сети и после перезагрузки заново подключитесь к светильнику в приложении.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={closeAlert} color="primary">
            ОК
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
