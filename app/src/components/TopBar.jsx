import React, { useContext } from 'react';
import { makeStyles } from '@material-ui/core/styles';

import AppBar from '@material-ui/core/AppBar';
import IconButton from '@material-ui/core/IconButton';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

import SaveIcon from '@material-ui/icons/Save';
import WifiOffOutlinedIcon from '@material-ui/icons/WifiOffOutlined';
import WifiOutlinedIcon from '@material-ui/icons/WifiOutlined';

import { ConnectionContext } from './AppContexts';

const useStyles = makeStyles((theme) => ({
  title: {
    flexGrow: 1,
  },
  save: {
    marginRight: theme.spacing(2),
  },
}));

export default function TopBar({ title, save }) {
  const classes = useStyles();

  const [connected] = useContext(ConnectionContext);

  return (
    <AppBar position="sticky">
      <Toolbar>
        <Typography variant="h6" className={classes.title}>
          {title || 'Светильник'}
        </Typography>
        {save ? (
          <IconButton className={classes.save} color="inherit" onClick={save}>
            <SaveIcon />
          </IconButton>
        ) : null}
        {connected ? <WifiOutlinedIcon /> : <WifiOffOutlinedIcon />}
      </Toolbar>
    </AppBar>
  );
}
