export default async function geteffects(fetcher, ip) {
  try {
    const json = await fetcher(ip, { action: 'geteffects' });
    if (json.error === 'OK') {
      return {
        brightness: +json.brightness,
        maxbrightness: +json.maxbrightness,
        index: +json.index,
        value: +json.value,
      };
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}
