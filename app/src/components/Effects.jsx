import React, { useState, useEffect, useContext, useCallback } from 'react';
import { makeStyles } from '@material-ui/core/styles';

import Accordion from '@material-ui/core/Accordion';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Grid from '@material-ui/core/Grid';
import Slider from '@material-ui/core/Slider';
import Tooltip from '@material-ui/core/Tooltip';
import Typography from '@material-ui/core/Typography';

import BrightnessHighIcon from '@material-ui/icons/BrightnessHigh';
import BrightnessLowIcon from '@material-ui/icons/BrightnessLow';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import { ConnectionContext, ApiContext } from './AppContexts';

const useStyles = makeStyles((theme) => ({
  slider: {
    paddingTop: theme.spacing(2),
    paddingBottom: theme.spacing(2),
  },
  icon: {
    paddingLeft: theme.spacing(2),
    paddingRight: theme.spacing(2),
  },
  params: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
  },
}));

function hueHelper(hue, value) {
  return hue * 256 + (value % 256);
}

function satHelper(sat, value) {
  return Math.floor(value / 256) * 256 + sat;
}

function ValueLabelComponent({ children, open, value }) {
  return (
    <Tooltip open={open} enterTouchDelay={0} placement="top" title={value}>
      {children}
    </Tooltip>
  );
}

export default function Effects() {
  const classes = useStyles();

  const [, setConnected] = useContext(ConnectionContext);
  const API = useContext(ApiContext);

  const minBrightness = 16;
  const [brightness, setBrightness] = useState(minBrightness);
  const [maxBrightness, setMaxBrightness] = useState(minBrightness);

  const [effect, setEffect] = useState({ index: 0, value: 0, save: false });
  const defaultValues = [0, 255, 192, 20, 20, -40, 4, 5, 10, 1];

  const handleChangeBrightness = (event, newValue) => {
    setBrightness(newValue);
  };

  const handleEffect = (panel) => (event, isExpanded) => {
    setEffect(
      isExpanded
        ? { index: panel, value: defaultValues[panel], save: true }
        : { index: 0, value: 0, save: true },
    );
  };

  const handleChangeParamSlider = (value) => {
    setEffect({ ...effect, value, save: false });
  };

  const handleCommitParamSlider = (value) => {
    setEffect({ ...effect, value, save: true });
  };

  const handleChangeParamCheckbox = (event) => {
    setEffect({ ...effect, value: +event.target.checked, save: true });
  };

  const loadEffects = useCallback(async () => {
    const result = await API.geteffects();
    if (!result) {
      setConnected(false);
    } else {
      setEffect({ index: result.index, value: result.value, save: false });
      setBrightness(result.brightness);
      setMaxBrightness(result.maxbrightness);
    }
  }, [API, setConnected]);

  // save brightness
  const handleCommitBrightness = async (event, newValue) => {
    const result = await API.setbrightness(newValue);
    if (!result) {
      setConnected(false);
    }
  };

  // save effect
  useEffect(() => {
    if (effect.save) {
      (async () => {
        const result = await API.seteffect(effect.index, Math.abs(effect.value));
        if (!result) {
          setConnected(false);
        }
      })();
    }
  }, [API, setConnected, effect]);

  useEffect(() => {
    window.addEventListener('focus', loadEffects);
    loadEffects();

    return () => {
      window.removeEventListener('focus', loadEffects);
    };
  }, [loadEffects]);

  return (
    <>
      <Grid container alignItems="center" className={classes.slider}>
        <Grid item className={classes.icon}>
          <BrightnessLowIcon />
        </Grid>
        <Grid item xs>
          <Slider
            min={minBrightness}
            max={maxBrightness}
            valueLabelDisplay="auto"
            ValueLabelComponent={ValueLabelComponent}
            value={brightness}
            onChange={handleChangeBrightness}
            onChangeCommitted={handleCommitBrightness}
          />
        </Grid>
        <Grid item className={classes.icon}>
          <BrightnessHighIcon />
        </Grid>
      </Grid>

      <Accordion expanded={effect.index === 1} onChange={handleEffect(1)}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Выбранный цвет</Typography>
        </AccordionSummary>
        <AccordionDetails className={classes.params}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Slider
                track={false}
                min={0}
                max={255}
                marks={[
                  { value: 0, label: 'К' },
                  { value: 32, label: 'О' },
                  { value: 64, label: 'Ж' },
                  { value: 96, label: 'З' },
                  { value: 128, label: 'Г' },
                  { value: 160, label: 'С' },
                  { value: 192, label: 'Ф' },
                  { value: 224, label: 'Р' },
                  { value: 255, label: 'К' },
                ]}
                value={Math.floor(effect.value / 256)}
                onChange={(e, newValue) =>
                  handleChangeParamSlider(hueHelper(newValue, effect.value))
                }
                onChangeCommitted={(e, newValue) =>
                  handleCommitParamSlider(hueHelper(newValue, effect.value))
                }
              />
            </Grid>
            <Grid item xs={12}>
              <Slider
                track={false}
                min={0}
                max={255}
                value={effect.value % 256}
                onChange={(e, newValue) =>
                  handleChangeParamSlider(satHelper(newValue, effect.value))
                }
                onChangeCommitted={(e, newValue) =>
                  handleCommitParamSlider(satHelper(newValue, effect.value))
                }
              />
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {[
        [2, 'Цвета по кругу', 0, 255],
        [3, 'Вертикальная радуга', 0, 32],
        [4, 'Горизонтальная радуга', 0, 32],
        [5, 'Матрица', -150, -5],
        [6, 'Вспышки', 1, 32],
        [7, 'Светлячки', 1, 16],
        [8, 'Плазма', 5, 50],
      ].map((x) => (
        <Accordion key={x[0]} expanded={effect.index === x[0]} onChange={handleEffect(x[0])}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>{x[1]}</Typography>
          </AccordionSummary>
          <AccordionDetails className={classes.params}>
            <Slider
              track={false}
              min={x[2]}
              max={x[3]}
              value={effect.value}
              onChange={(e, newValue) => handleChangeParamSlider(newValue)}
              onChangeCommitted={(e, newValue) => handleCommitParamSlider(newValue)}
            />
          </AccordionDetails>
        </Accordion>
      ))}

      <Accordion expanded={effect.index === 9} onChange={handleEffect(9)}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Огонь</Typography>
        </AccordionSummary>
        <AccordionDetails className={classes.params}>
          <FormControlLabel
            control={
              <Checkbox
                checked={!!effect.value}
                onChange={handleChangeParamCheckbox}
                color="primary"
              />
            }
            label="Искры"
          />
        </AccordionDetails>
      </Accordion>
    </>
  );
}
