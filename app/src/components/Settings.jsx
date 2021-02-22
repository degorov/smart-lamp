import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';

import Button from '@material-ui/core/Button';
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

import Api from '../api';
import Credits from './Credits';

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.paper,
  },
  icon: {
    marginTop: '-20px',
  },
}));

export default function Settings({ setChanged, connected, setConnected }) {
  const classes = useStyles();

  const [ip, setIp] = useState(localStorage.getItem('lamp-ip') || '192.168.0.200');
  const [isIpValid, setIsIpValid] = useState(false);

  const handleChangeIp = (event) => {
    setIp(event.target.value);
  };

  useEffect(() => {
    if (/^(?!0)(?!.*\.$)((1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$/.test(ip)) {
      setIsIpValid(true);
    } else {
      setIsIpValid(false);
    }
  }, [ip]);

  const handleConnect = async () => {
    setConnected(false);
    const connected = await Api.ping(ip);
    if (connected) {
      localStorage.setItem('lamp-ip', ip);
    }
    setConnected(connected);
  };

  const [wifi, setWifi] = useState({
    ssid: 'Smart-Lamp',
    password: '',
    showPassword: false,
  });

  const handleChangeWifi = (prop) => (event) => {
    setWifi({ ...wifi, [prop]: event.target.value });
    setChanged(true);
  };

  const handleClickShowPassword = () => {
    setWifi({ ...wifi, showPassword: !wifi.showPassword });
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const [timezone, setTimezone] = useState(3);
  const handleChangeTimezone = (event) => {
    setTimezone(event.target.value);
    setChanged(true);
  };

  const [brightness, setBrightness] = useState(192);
  const handleChangeBrightness = (event, newValue) => {
    setBrightness(newValue);
    setChanged(true);
  };

  useEffect(
    () => () => {
      setChanged(false);
    },
    [setChanged],
  );

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
            value={ip}
            onChange={handleChangeIp}
            error={!isIpValid}
          />
          <ListItemSecondaryAction>
            <Button
              variant="contained"
              color="primary"
              disabled={!isIpValid}
              onClick={handleConnect}
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
                value={wifi.ssid}
                onChange={handleChangeWifi('ssid')}
              />
            </ListItem>
            <ListItem>
              <FormControl variant="outlined" size="small" fullWidth={true}>
                <InputLabel htmlFor="password">Пароль сети</InputLabel>
                <OutlinedInput
                  id="password"
                  labelWidth={95}
                  type={wifi.showPassword ? 'text' : 'password'}
                  value={wifi.password}
                  onChange={handleChangeWifi('password')}
                  endAdornment={
                    <InputAdornment position="end">
                      <IconButton
                        onClick={handleClickShowPassword}
                        onMouseDown={handleMouseDownPassword}
                        edge="end"
                      >
                        {wifi.showPassword ? <Visibility /> : <VisibilityOff />}
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
                value={timezone}
                onChange={handleChangeTimezone}
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
              <Typography component="span" color={brightness > 192 ? 'error' : 'initial'}>
                &nbsp;{brightness}
              </Typography>
            </ListSubheader>
            <ListItem>
              <Grid container spacing={2} alignItems="center">
                <Grid item className={classes.icon}>
                  <BrightnessLowIcon />
                </Grid>
                <Grid item xs>
                  <Slider
                    min={0}
                    max={255}
                    marks={[
                      {
                        value: 192,
                        label: 'Предел БП',
                      },
                    ]}
                    value={brightness}
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
    </>
  );
}
