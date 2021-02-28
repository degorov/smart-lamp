export default async function seteffect(fetcher, index, value, ip) {
  try {
    const json = await fetcher(ip, { action: 'seteffect', index, value });
    if (json.error === 'OK') {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}
