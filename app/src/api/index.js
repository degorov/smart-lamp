import ping from './ping';

const TIMEOUT = 3000;
const FUNCTIONS = { ping };

export default function Api(showLoader) {
  const fetcher = async (ip, payload) => {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), TIMEOUT);
    showLoader(true);
    try {
      const response = await fetch(`http://${ip}/`, {
        signal: controller.signal,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      return await response.json();
    } finally {
      clearTimeout(timeout);
      showLoader(false);
    }
  };

  // Using FUNCTIONS Object instead of Array because minification in production ruins fn.name
  return Object.fromEntries(
    Object.entries(FUNCTIONS).map(([fnname, fn]) => [fnname, fn.bind(null, fetcher)]),
  );
}
