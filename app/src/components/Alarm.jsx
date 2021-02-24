import React, { useState, useEffect, useContext } from 'react';
import { makeStyles } from '@material-ui/core/styles';

import Checkbox from '@material-ui/core/Checkbox';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import Switch from '@material-ui/core/Switch';
import TextField from '@material-ui/core/TextField';

import AlarmIcon from '@material-ui/icons/Alarm';

import { ConnectionContext, ApiContext } from './AppContexts';

const useStyles = makeStyles((theme) => ({
  alarmField: {
    background: theme.palette.background.paper,
    width: 150,
  },
  timeField: {
    background: theme.palette.background.paper,
    width: 75,
  },
}));

export default function Alarm({ setSave }) {
  const classes = useStyles();

  const [connected] = useContext(ConnectionContext);
  const API = useContext(ApiContext);

  const [alarm, setAlarm] = useState({
    enabled: false,
    time: '',
    repeat: 0,
    before: 0,
    after: 0,
  });

  const handleToggleAlarm = () => {
    // setState((prev) => !prev);
  };

  const handleChangeAlarm = (prop) => (event) => {
    // setState({ ...settings, [prop]: event.target.value });
  };

  const handleToggleRepeat = (value) => () => {
    // https://material-ui.com/components/lists/
  };

  const saveAlarm = () => async () => {
    await console.log('SAVE ALARM');
    setSave(null);
  };

  useEffect(() => {
    if (connected) {
      console.log('LOAD ALARM');
    }
    return () => {
      setSave(null);
    };
  }, [connected, setSave]);

  return (
    <List>
      <ListItem>
        <ListItemIcon>
          <AlarmIcon />
        </ListItemIcon>
        <ListItemText primary="Будильник включен" />
        <ListItemSecondaryAction>
          <Switch color="primary" edge="end" checked={true} onChange={handleToggleAlarm} />
        </ListItemSecondaryAction>
      </ListItem>
      <ListItem>
        <ListItemText inset primary="Время:" />
        <TextField
          id="alarm-time"
          type="time"
          variant="outlined"
          size="small"
          className={classes.alarmField}
          inputProps={{
            step: 300, // 5 min
          }}
          value={''}
          onChange={handleChangeAlarm('time')}
        />
      </ListItem>

      <ListSubheader>Повторять по:</ListSubheader>
      {['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'].map(
        (value, index) => (
          <ListItem dense button key={index} onClick={handleToggleRepeat(index)}>
            <ListItemIcon>
              <Checkbox color="primary" edge="start" checked={true} disableRipple />
            </ListItemIcon>
            <ListItemText primary={value} />
          </ListItem>
        ),
      )}

      <ListSubheader>Настройки рассвета (в минутах):</ListSubheader>
      <ListItem>
        <ListItemText primary="Рассвет до будильника:" />
        <ListItemSecondaryAction>
          <TextField
            id="time-before"
            size="small"
            variant="outlined"
            className={classes.timeField}
            inputProps={{ maxLength: 2 }}
            value={''}
            onChange={handleChangeAlarm('before')}
          />
        </ListItemSecondaryAction>
      </ListItem>
      <ListItem>
        <ListItemText primary="Гореть после будильника:" />
        <ListItemSecondaryAction>
          <TextField
            id="time-after"
            size="small"
            variant="outlined"
            className={classes.timeField}
            inputProps={{ maxLength: 2 }}
            value={''}
            onChange={handleChangeAlarm('after')}
          />
        </ListItemSecondaryAction>
      </ListItem>
    </List>
  );
}
