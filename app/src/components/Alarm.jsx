import React, { useState, useEffect, useContext, useCallback } from 'react';
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
import Typography from '@material-ui/core/Typography';

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
  message: {
    padding: theme.spacing(2),
  },
}));

export default function Alarm({ setSave }) {
  const classes = useStyles();

  const [, setConnected] = useContext(ConnectionContext);
  const API = useContext(ApiContext);

  const [alarm, setAlarm] = useState({
    apmode: false,
    enabled: false,
    repeat: 0,
    time: '',
    before: 0,
    after: 0,
  });

  const handleToggleAlarm = (event) => {
    setAlarm({ ...alarm, enabled: event.target.checked });
    setSave(saveAlarm);
  };

  const handleChangeAlarm = (prop) => (event) => {
    setAlarm({ ...alarm, [prop]: event.target.value });
    setSave(saveAlarm);
  };

  const handleToggleRepeat = (index) => (event) => {
    if (event.target.checked) {
      setAlarm({ ...alarm, repeat: (1 << (6 - index)) | alarm.repeat });
    } else {
      setAlarm({ ...alarm, repeat: ~(1 << (6 - index)) & alarm.repeat });
    }
    setSave(saveAlarm);
  };

  const loadAlarm = useCallback(async () => {
    const result = await API.getalarm();
    if (!result) {
      setConnected(false);
    } else {
      setAlarm({
        apmode: result.apmode,
        enabled: result.enabled,
        repeat: result.repeat,
        time: result.time,
        before: result.before,
        after: result.after,
      });
    }
  }, [API, setConnected]);

  const saveAlarm = () => () => {
    setAlarm((alarm) => {
      (async () => {
        const result = await API.savealarm(
          alarm.enabled,
          alarm.repeat,
          alarm.time,
          alarm.before,
          alarm.after,
        );
        if (!result) {
          setConnected(false);
        }
      })();
      return alarm;
    });
    setSave(null);
  };

  useEffect(() => {
    window.addEventListener('focus', loadAlarm);
    loadAlarm();

    return () => {
      window.removeEventListener('focus', loadAlarm);
      setSave(null);
    };
  }, [loadAlarm, setSave]);

  return !alarm.apmode ? (
    <List>
      <ListItem>
        <ListItemIcon>
          <AlarmIcon />
        </ListItemIcon>
        <ListItemText primary="Будильник включен" />
        <ListItemSecondaryAction>
          <Switch color="primary" edge="end" checked={alarm.enabled} onChange={handleToggleAlarm} />
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
            step: 300, // 5 minutes
          }}
          value={alarm.time}
          onChange={handleChangeAlarm('time')}
        />
      </ListItem>

      <ListSubheader>Повторять по:</ListSubheader>
      {['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'].map(
        (label, index) => (
          <ListItem dense button key={index} disableRipple>
            <ListItemIcon>
              <Checkbox
                color="primary"
                edge="start"
                checked={!!((1 << (6 - index)) & alarm.repeat)}
                onClick={handleToggleRepeat(index)}
              />
            </ListItemIcon>
            <ListItemText primary={label} />
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
            type="number"
            inputProps={{ maxLength: 2 }}
            value={alarm.before}
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
            type="number"
            inputProps={{ maxLength: 2 }}
            value={alarm.after}
            onChange={handleChangeAlarm('after')}
          />
        </ListItemSecondaryAction>
      </ListItem>
    </List>
  ) : (
    <Typography align={'center'} className={classes.message}>
      Настройка будильника будет доступна после подключения светильника к сети Wi-Fi с доступом в
      Интернет для синхронизации с серверами точного времени.
    </Typography>
  );
}
