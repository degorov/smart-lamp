import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import BottomNavigation from '@material-ui/core/BottomNavigation';
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction';

import AlarmIcon from '@material-ui/icons/Alarm';
import SettingsOutlinedIcon from '@material-ui/icons/SettingsOutlined';
import WbIncandescentOutlinedIcon from '@material-ui/icons/WbIncandescentOutlined';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    maxWidth: theme.breakpoints.values.sm,
    position: 'fixed',
    bottom: 0,
    zIndex: 100,
  },
}));

export default function BottomNav({ page, labels, connected, setPage }) {
  const classes = useStyles();

  const handleChange = (event, newValue) => {
    if (connected) setPage(newValue);
  };

  return (
    <BottomNavigation className={classes.root} showLabels value={page} onChange={handleChange}>
      {connected ? (
        <BottomNavigationAction label={labels[0]} icon={<WbIncandescentOutlinedIcon />} />
      ) : null}
      {connected ? <BottomNavigationAction label={labels[1]} icon={<AlarmIcon />} /> : null}
      <BottomNavigationAction label={labels[2]} icon={<SettingsOutlinedIcon />} />
    </BottomNavigation>
  );
}
