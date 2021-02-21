import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import WifiOutlinedIcon from '@material-ui/icons/WifiOutlined';
import WifiOffOutlinedIcon from '@material-ui/icons/WifiOffOutlined';

const useStyles = makeStyles({
  title: {
    flexGrow: 1,
  },
});

export default function TopBar({ title, connected }) {
  const classes = useStyles();

  return (
    <AppBar position="sticky">
      <Toolbar>
        <Typography variant="h6" className={classes.title}>
          {title}
        </Typography>
        {connected ? <WifiOutlinedIcon /> : <WifiOffOutlinedIcon />}
      </Toolbar>
    </AppBar>
  );
}
