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

export default function BottomNav({ page, labels, setPage }) {
  const classes = useStyles();

  return (
    <BottomNavigation
      value={page}
      onChange={(event, newValue) => {
        setPage(newValue);
      }}
      showLabels
      className={classes.root}
    >
      <BottomNavigationAction label={labels[0]} icon={<WbIncandescentOutlinedIcon />} />
      <BottomNavigationAction label={labels[1]} icon={<AlarmIcon />} />
      <BottomNavigationAction label={labels[2]} icon={<SettingsOutlinedIcon />} />
    </BottomNavigation>
  );
}
