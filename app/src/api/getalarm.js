export default async function getalarm(fetcher, ip) {
  try {
    const json = await fetcher(ip, { action: 'getalarm' });
    if (json.error === 'OK') {
      return {
        apmode: !!json.apmode,
        enabled: !!json.enabled,
        time: json.time,
        repeat: +json.repeat,
        before: +json.before,
        after: +json.after,
      };
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}
