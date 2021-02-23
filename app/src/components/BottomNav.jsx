import React, { useContext } from 'react';
import { makeStyles } from '@material-ui/core/styles';

import BottomNavigation from '@material-ui/core/BottomNavigation';
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction';

import AlarmIcon from '@material-ui/icons/Alarm';
import SettingsOutlinedIcon from '@material-ui/icons/SettingsOutlined';
import WbIncandescentOutlinedIcon from '@material-ui/icons/WbIncandescentOutlined';

import { ConnectedContext } from './AppContexts';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    maxWidth: theme.breakpoints.values.sm,
    position: 'fixed',
    bottom: 0,
    zIndex: 100,
  },
}));

export default function BottomNav({ page, labels, setPage }) {
  const classes = useStyles();

  const connected = useContext(ConnectedContext);

  return connected ? (
    <BottomNavigation
      className={classes.root}
      showLabels
      value={page}
      onChange={(event, newValue) => {
        setPage(newValue);
      }}
    >
      <BottomNavigationAction label={labels[0]} icon={<WbIncandescentOutlinedIcon />} />
      <BottomNavigationAction label={labels[1]} icon={<AlarmIcon />} />
      <BottomNavigationAction label={labels[2]} icon={<SettingsOutlinedIcon />} />
    </BottomNavigation>
  ) : null;
}
