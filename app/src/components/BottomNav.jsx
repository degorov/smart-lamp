import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import BottomNavigation from '@material-ui/core/BottomNavigation';
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction';
import WbIncandescentOutlinedIcon from '@material-ui/icons/WbIncandescentOutlined';
import AlarmIcon from '@material-ui/icons/Alarm';
import SettingsOutlinedIcon from '@material-ui/icons/SettingsOutlined';

const useStyles = makeStyles({
  root: {
    width: '100%',
    position: 'sticky',
    bottom: 0,
  },
});

export default function BottomNav({ page, labels, onChange }) {
  const classes = useStyles();

  return (
    <BottomNavigation
      value={page}
      onChange={(event, newValue) => {
        onChange(newValue);
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
